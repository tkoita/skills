#!/usr/bin/env python3
"""Read-only, conservative static TeX dependency inspection. No TeX execution."""
import argparse
import json
import re
from pathlib import Path


def strip_comments(text):
    lines = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for i, char in enumerate(line):
            if char == '%':
                backslashes = len(line[:i]) - len(line[:i].rstrip('\\'))
                if backslashes % 2 == 0:
                    cut = i
                    break
        lines.append(line[:cut] + ('\n' if cut < len(line) and line.endswith('\n') else ''))
    return ''.join(lines)


class Inspector:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.facts = []
        self.candidates = []
        self.unchecked = []
        self.visited = set()
        self.active = set()
        self.dependencies = set()
        self.labels = {}
        self.cites = []
        self.refs = []
        self.keys = set()
        self.bib_seen = set()

    def record(self, bucket, code, path, line, detail):
        bucket.append(dict(code=code, path=str(path), line=line, detail=detail))

    def resolve(self, name, extensions, source, line, optional=False):
        if any(c in name for c in ('\\', '#', '$', '{', '}')):
            self.record(self.unchecked, 'dynamic_path', source, line, name)
            return None
        # TeX inputs normally resolve from the compilation directory, not the chapter directory.
        bases = [self.root / name]
        found = []
        for base in bases:
            choices = [base] if base.suffix else [base.with_suffix(e) for e in extensions]
            for p in choices:
                resolved = p.resolve()
                if not resolved.is_relative_to(self.root):
                    self.record(self.unchecked, 'outside_root', source, line, name)
                    return None
                if resolved.is_file():
                    found.append(resolved)
        if found:
            self.dependencies.add(found[0])
            return found[0]
        if not optional:
            self.record(self.candidates, 'missing_dependency', source, line, name)
        return None

    def visit_bib(self, path):
        if path in self.bib_seen:
            return
        self.bib_seen.add(path)
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            self.record(self.unchecked, 'bib_read_failed', path, None, str(exc))
            return
        for match in re.finditer(r'@(?!(?:comment|preamble|string)\b)\w+\s*[{(]\s*([^,\s]+)\s*,', text, re.I):
            key = match.group(1)
            if key in self.keys:
                self.record(self.candidates, 'duplicate_bib_key', path, text.count('\n', 0, match.start())+1, key)
            self.keys.add(key)

    def visit(self, path):
        if path in self.active:
            self.record(self.candidates, 'input_cycle', path, None, '入力ファイルの循環参照')
            return
        if path in self.visited:
            return
        self.visited.add(path)
        self.active.add(path)
        self.dependencies.add(path)
        try:
            raw = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            self.record(self.unchecked, 'source_read_failed', path, None, str(exc))
            self.active.remove(path)
            return
        text = strip_comments(raw)
        if not text.strip():
            self.record(self.candidates, 'empty_source', path, None, 'コメント以外の内容なし')
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(r'要記入|XXXX|サブセクション[12]|謝辞謝辞|word1|ここに結論|\bTODO\b', line):
                self.record(self.candidates, 'placeholder', path, n, line.strip()[:180])
        for match in re.finditer(r'\\(documentclass|geometry|usepackage)\s*(?:\[([^\]]*)\])?\s*\{([^{}]*)\}', text):
            cmd, opts, value = match.groups()
            if cmd == 'documentclass' or value == 'geometry' or cmd == 'geometry':
                self.record(self.facts, 'layout_setting', path, text.count('\n',0,match.start())+1, match.group())
        if re.search(r'\\(?:graphicspath|includeonly|import|subimport|if\w*|begin\{(?:verbatim|lstlisting|minted)\})', text):
            self.record(self.unchecked, 'advanced_tex', path, None, '条件分岐・特殊な入力・図パス・verbatim等を手動確認')
        command = re.compile(r'\\(input|include|usepackage|RequirePackage|bibliography(?!style)\w*|addbibresource|includegraphics|label|(?:eq|page|auto|c|C)?ref|(?:text|paren|auto)?cite\w*|nocite\w*|bibitem)\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]*)\}')
        for match in command.finditer(text):
            cmd, arg = match.groups()
            line = text.count('\n', 0, match.start())+1
            if cmd in ('input','include'):
                dep = self.resolve(arg.strip(), ['.tex'], path, line)
                if dep:
                    self.visit(dep)
            elif cmd in ('usepackage','RequirePackage'):
                for name in arg.split(','):
                    dep = self.resolve(name.strip(), ['.sty'], path, line, optional=True)
                    if dep:
                        self.visit(dep)
            elif cmd.startswith('bibliography') or cmd == 'addbibresource':
                for name in arg.split(','):
                    dep = self.resolve(name.strip(), ['.bib'], path, line)
                    if dep:
                        self.visit_bib(dep)
            elif cmd == 'includegraphics':
                self.resolve(arg.strip(), ['.pdf','.png','.jpg','.jpeg','.eps'], path, line)
            elif cmd == 'label':
                if arg in self.labels:
                    self.record(self.candidates, 'duplicate_label', path, line, arg)
                self.labels[arg] = (path,line)
            elif cmd.endswith('ref'):
                for key in arg.split(','):
                    self.refs.append((key.strip(),path,line))
            elif cmd == 'bibitem':
                self.keys.add(arg.strip())
            else:
                for key in arg.split(','):
                    if key.strip() != '*':
                        self.cites.append((key.strip(),path,line))
        self.active.remove(path)

    def finish(self, pdf=None):
        for key,path,line in self.refs:
            if key not in self.labels:
                self.record(self.candidates, 'unresolved_reference_candidate', path,line,key)
        for key,path,line in self.cites:
            if key not in self.keys:
                self.record(self.candidates, 'unresolved_citation_candidate', path,line,key)
        if pdf:
            try:
                from pypdf import PdfReader
            except ImportError:
                self.record(self.unchecked,'pdf_dependency_unavailable',pdf,None,'pypdf未導入。PDF測定は未実施')
            else:
                try:
                    reader = PdfReader(pdf)
                    self.facts.append(dict(code='pdf_measurements',path=str(pdf),pages=len(reader.pages),bytes=pdf.stat().st_size,page_sizes_pt=[[round(float(p.mediabox.width),2),round(float(p.mediabox.height),2)] for p in reader.pages]))
                except Exception as exc:
                    self.record(self.unchecked,'pdf_read_failed',pdf,None,str(exc))
            if pdf.is_file():
                newer = [str(p) for p in sorted(self.dependencies) if p.stat().st_mtime > pdf.stat().st_mtime]
                if newer:
                    self.record(self.candidates,'dependencies_newer_than_pdf',pdf,None,newer)
        self.unchecked.append(dict(code='static_only',detail='TeX実行・マクロ展開・条件分岐評価・PDF目視・フォント検査・規定適合・主張の検証は未実施。候補0件でも合格ではない。'))
        return dict(schema_version=1,root=str(self.root),files=[str(p) for p in sorted(self.dependencies)],facts=self.facts,candidates=self.candidates,unchecked=self.unchecked)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--main', default='main.tex')
    parser.add_argument('--pdf')
    args = parser.parse_args()
    inspector = Inspector(args.root)
    main_path = inspector.resolve(args.main, ['.tex'], inspector.root, None)
    if main_path:
        inspector.visit(main_path)
    pdf = None
    if args.pdf:
        pdf = inspector.resolve(args.pdf, ['.pdf'], inspector.root, None)
    print(json.dumps(inspector.finish(pdf), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
