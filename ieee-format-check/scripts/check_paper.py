#!/usr/bin/env python3
"""Mechanical IEEE-format checks for an IEEEtran paper (.tex and/or .pdf).

Prints a Markdown report of FACTS (what the paper is) and CANDIDATES (things a
human or Claude should judge against the venue rules and IEEEtran_HOWTO).
A candidate is not a verdict: many depend on the venue, so every one carries
the rule key it relates to (see references/ieeetran-rules.md).

Usage:
    python3 check_paper.py --tex paper.tex [--pdf paper.pdf]
    python3 check_paper.py --pdf paper.pdf

Needs only the Python standard library; PDF checks use poppler's
pdfinfo / pdffonts / pdfimages when they are on PATH.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

findings = []  # (level, rule, where, message)
facts = []


def add(level, rule, where, msg):
    findings.append((level, rule, where, msg))


# ---------------------------------------------------------------- TeX helpers

def strip_comments(text):
    """Remove % comments but keep line structure so line numbers stay valid."""
    out = []
    for line in text.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        out.append(line[: m.start()] if m else line)
    return "\n".join(out)


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def braced(text, start):
    """Return (content, end) of the {...} group whose '{' is at text[start]."""
    assert text[start] == "{"
    depth, i = 0, start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    return text[start + 1 :], len(text)


def command_args(text, name):
    """Yield (pos, content) for every \\name{...} (optional [..] skipped)."""
    for m in re.finditer(r"\\" + name + r"\*?\s*(\[[^\]]*\])?\s*\{", text):
        content, _ = braced(text, m.end() - 1)
        yield m.start(), content


def env_blocks(text, env):
    pat = re.compile(r"\\begin\{" + re.escape(env) + r"\}(.*?)\\end\{" + re.escape(env) + r"\}", re.S)
    for m in pat.finditer(text):
        yield m.start(), m.group(1)


def plain(s):
    s = re.sub(r"\\(emph|textit|textbf|upshape|mathrm|text)\b", "", s)
    s = re.sub(r"~|\\,|\\ ", " ", s)
    s = re.sub(r"\\ref\{[^}]*\}", "N", s)
    s = re.sub(r"[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


MINOR = set("a an and as at but by for in nor of on or the to up via with from vs".split())


def looks_title_case(s):
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-]*", plain(re.sub(r"\$[^$]*\$", "", s)))]
    if len(words) < 3:
        return True
    major = [w for i, w in enumerate(words) if i == 0 or w.lower() not in MINOR]
    caps = sum(1 for w in major if w[0].isupper())
    return caps / max(1, len(major)) >= 0.7


def sentences(s):
    s = plain(re.sub(r"\$[^$]*\$", "X", s))
    s = re.sub(r"\b(e\.g|i\.e|et al|Fig|Eq|vs|cf|approx)\.", r"\1", s)
    return [x for x in re.split(r"(?<=[.;?!])\s+(?=[A-Z(\"`])", s) if x.strip()]


# ---------------------------------------------------------------- TeX checks

PLACEHOLDERS = [
    r"example\.com", r"First Author", r"Second Author", r"Given Name Surname",
    r"dept\. name of organization", r"name of organization", r"City, Country",
    r"email address or ORCID", r"Department, University",
]
TEMPLATE_REMNANTS = [
    r"IEEE conference templates contain guidance text",
    r"Identify applicable funding agency here",
    r"If none, delete this",
    r"Please ensure that all template text is removed",
    r"Use this document as a template",
]
CAUTION_PKGS = {
    "geometry": "HOWTO App. B: do not alter margins/paper size with geometry.sty etc.",
    "fullpage": "HOWTO App. B: do not alter margins.",
    "a4wide": "HOWTO App. B: do not alter margins.",
    "times": "HOWTO App. B: let IEEEtran manage fonts.",
    "mathptm": "HOWTO App. B: let IEEEtran manage fonts.",
    "mathptmx": "HOWTO App. B: let IEEEtran manage fonts.",
    "pslatex": "HOWTO App. B: let IEEEtran manage fonts.",
    "newtxtext": "HOWTO II-D: do not load newtxtext (alters main text font).",
    "subfigure": "HOWTO X-A1: subfigure.sty not recommended; use subfig with caption=false.",
    "subcaption": "HOWTO X-A1: subcaption cannot keep IEEEtran's caption style.",
    "caption": "HOWTO X-A1: caption.sty overrides IEEEtran caption style.",
    "algorithm": "HOWTO X-B: do not use algorithm.sty float; put algorithmic in figure.",
    "algorithm2e": "HOWTO X-B: algorithm2e float gives non-IEEE captions.",
    "psfig": "HOWTO App. B: use graphicx only.",
    "epsfig": "HOWTO App. B: use graphicx only.",
    "epsf": "HOWTO App. B: use graphicx only.",
}


def check_tex(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    t = strip_comments(raw)
    rel = Path(path).name

    def at(pos):
        return f"{rel}:{lineno(t, pos)}"

    # --- class and options
    m = re.search(r"\\documentclass\s*(\[([^\]]*)\])?\s*\{([^}]*)\}", t)
    opts = []
    if not m:
        add("check", "class", rel, "No \\documentclass found.")
        compsoc = conference = False
    else:
        cls = m.group(3).strip()
        opts = [o.strip() for o in (m.group(2) or "").split(",") if o.strip()]
        facts.append(f"documentclass: `{cls}` options={opts or '(none)'}")
        if cls != "IEEEtran":
            add("check", "class", at(m.start()), f"Class is `{cls}`, not IEEEtran; IEEE checks below may not apply.")
        conference = "conference" in opts
        compsoc = "compsoc" in opts
        if not conference:
            add("check", "HOWTO II-C", at(m.start()), "No `conference` option: journal mode layout (running heads, \\thanks enabled). Confirm the venue is a journal.")
        for o in opts:
            if o in ("draft", "draftcls", "draftclsnofoot", "onecolumn", "peerreview", "peerreviewca"):
                add("check", "HOWTO II-B/II-C", at(m.start()), f"Option `{o}` is for drafts/review, not camera-ready.")
            if o in ("11pt", "12pt", "9pt"):
                add("warn", "HOWTO II-A", at(m.start()), f"Font size `{o}`; IEEE conference camera-ready is normally 10pt.")
            if o == "a4paper":
                add("warn", "HOWTO II-E", at(m.start()), "a4paper: IEEE primarily wants US letter unless the venue says otherwise.")
            if o == "comsoc" and conference:
                add("warn", "HOWTO II-D1a", at(m.start()), "comsoc with conference: only if the conference instructs it.")
            if o == "compsoc":
                add("info", "HOWTO II-D2a", at(m.start()), "compsoc: many Computer Society conferences use plain conference format; use 'Figure' in text.")

    # --- packages
    for pm in re.finditer(r"\\usepackage\s*(\[([^\]]*)\])?\s*\{([^}]*)\}", t):
        popts = pm.group(2) or ""
        for p in [x.strip() for x in pm.group(3).split(",")]:
            if p in CAUTION_PKGS:
                add("warn", "HOWTO App. B / X", at(pm.start()), f"\\usepackage{{{p}}}: {CAUTION_PKGS[p]}")
            if p == "subfig" and "caption=false" not in popts.replace(" ", ""):
                add("warn", "HOWTO X-A1", at(pm.start()), "subfig loaded without caption=false (overrides IEEE caption style).")
    if re.search(r"\\cite\{", t) and not re.search(r"\\usepackage(\[[^\]]*\])?\{[^}]*\bcite\b", t):
        add("info", "HOWTO VII", rel, "cite.sty not loaded: adjacent citations will not be sorted/compressed.")

    # --- layout hacks
    for pat, msg in [
        (r"\\setlength\s*\{?\\(textheight|textwidth|topmargin|oddsidemargin|evensidemargin|columnsep|headheight|footskip)", "Manual page-geometry change"),
        (r"\\addtolength\s*\{?\\(textheight|textwidth|topmargin|oddsidemargin|columnsep)", "Manual page-geometry change"),
        (r"\\(linespread|renewcommand\s*\{?\\baselinestretch)", "Line spacing changed"),
        (r"\\vspace\*?\s*\{\s*-", "Negative \\vspace (space squeezing)"),
        (r"\\(pagestyle|thispagestyle)\s*\{", "Page style set manually (conference mode has no headers/page numbers)"),
    ]:
        for mm in re.finditer(pat, t):
            add("warn", "HOWTO App. B / II-C1", at(mm.start()), msg + ".")
    for mm in re.finditer(r"\\enlargethispage", t):
        add("info", "HOWTO XIV", at(mm.start()), "\\enlargethispage: fine for last-page column balancing, not for squeezing pages.")
    if conference:
        for mm in re.finditer(r"\\markboth", t):
            add("info", "HOWTO IV-C", at(mm.start()), "\\markboth has no effect in conference mode.")
        if re.search(r"\\thanks\s*\{", t) and "\\IEEEoverridecommandlockouts" not in t:
            add("warn", "HOWTO II-C1", rel, "\\thanks used in conference mode without \\IEEEoverridecommandlockouts (it is disabled).")

    # --- placeholders and template remnants
    for pat in PLACEHOLDERS:
        for mm in re.finditer(pat, t):
            add("check", "placeholder", at(mm.start()), f"Placeholder text still present: `{mm.group(0)}`.")
    for pat in TEMPLATE_REMNANTS:
        for mm in re.finditer(pat, t, re.I):
            add("check", "template", at(mm.start()), f"IEEE template guidance text not removed: `{mm.group(0)}`.")

    # --- template text left in comments (does not print, but shows unfinished cleanup)
    for i, line in enumerate(raw.split("\n"), 1):
        m = re.search(r"(?<!\\)%(.*)", line)
        if not m:
            continue
        c = m.group(1)
        if re.search(r"preceding line is only needed|identify funding|template text|conference_101719|Given Name Surname", c, re.I):
            add("info", "template", f"{rel}:{i}", f"Template comment left in source: `{c.strip()[:80]}` (no effect on PDF).")

    # --- title
    for pos, title in command_args(t, "title"):
        facts.append(f"title: {plain(title)}")
        if "$" in title:
            add("warn", "HOWTO IV-A", at(pos), "Math in the title ('Do not use math or other special symbols in the title').")
        if not looks_title_case(title):
            add("info", "HOWTO IV-A", at(pos), "Title may not be in title case.")
        break

    # --- author block
    for pos, auth in command_args(t, "author"):
        n_blockN = len(re.findall(r"\\IEEEauthorblockN", auth))
        blockA = [c for _, c in command_args(auth, "IEEEauthorblockA")]
        n_and = len(re.findall(r"\\and\b", auth))
        n_ref = len(set(re.findall(r"\\IEEEauthorrefmark\{(\w+)\}", auth)))
        names = []
        for _, c in command_args(auth, "IEEEauthorblockN"):
            c2 = re.sub(r"\\IEEEauthorrefmark\{\w+\}|\\textsuperscript\{[^}]*\}|\\\\", ",", c)
            names += [n.strip() for n in re.split(r",|\band\b", plain(c2)) if n.strip() and not re.fullmatch(r"\d+(st|nd|rd|th)?", n.strip())]
        style = "long format (\\IEEEauthorrefmark)" if n_ref else ("multicolumn (\\and)" if n_and else "single block")
        facts.append(f"author block: {style}; names≈{len(names)}; IEEEauthorblockN={n_blockN}; IEEEauthorblockA={len(blockA)}; \\and={n_and}; distinct refmarks={n_ref}")
        if re.search(r"\d\\textsuperscript\{(st|nd|rd|th)\}|\b\d(st|nd|rd|th)\s+[A-Z]", auth):
            add("info", "HOWTO IV-B2 / CT", at(pos), "Ordinal labels (1st, 2nd …) in author names: from IEEE's conference template sample (conference_101719); HOWTO examples have none. Not wrong; usually removed.")
        def norm(a):
            a = re.sub(r"\\IEEEauthorrefmark\{\w+\}", "", a)
            a = re.sub(r"(?i)e-?mail:?.*", "", a)
            a = re.sub(r"\S+@\S+", "", a)
            a = re.sub(r"\\url\{[^}]*\}|\\href\{[^}]*\}\{[^}]*\}", "", a)
            return re.sub(r"\s+", " ", plain(a.replace("\\\\", " "))).strip().lower()
        normed = [norm(a) for a in blockA]
        dups = {a for a in normed if a and normed.count(a) > 1}
        if dups and n_and:
            add("info", "HOWTO IV-B2 / CT", at(pos), f"Same affiliation repeated in {sum(normed.count(a) for a in dups)} columns: matches the conference template ('Names should not be listed in columns nor group by affiliation'), not HOWTO (one column per affiliation). Both are IEEE sources.")
        if n_and >= 3 and not dups:
            add("info", "HOWTO IV-B2", at(pos), f"{n_and + 1} affiliation columns: HOWTO prefers multicolumn only for three or fewer affiliations; consider the long format if too wide.")
        if n_ref and len(blockA) > 1:
            add("conv", "CT authors", at(pos), "Authors grouped by affiliation with \\IEEEauthorrefmark (HOWTO long format). The conference template says names should not be grouped by affiliation and affiliations kept succinct ('do not differentiate among departments of the same organization'). Both are IEEE sources.")
        if len(names) > 3 and n_and and not n_ref:
            add("info", "HOWTO IV-B2", at(pos), "More than three authors in multicolumn form: allowed if ≤3 affiliations; long format is the HOWTO alternative when it gets too wide.")
        break

    # --- abstract / keywords
    for pos, ab in env_blocks(t, "abstract"):
        words = len(plain(ab).split())
        facts.append(f"abstract: {words} words")
        if "\\cite" in ab:
            add("warn", "HOWTO V", at(pos), "Citation in abstract ('Math, special symbols and/or citations should generally not be used in abstracts').")
        if re.search(r"\$|\\\(|\\begin\{equation", ab):
            add("warn", "HOWTO V", at(pos), "Math in abstract.")
    kw = list(env_blocks(t, "IEEEkeywords"))
    if not kw:
        add("info", "HOWTO V", rel, "No IEEEkeywords (Index Terms) block; check whether the venue requires keywords.")
    for pos, k in kw:
        if "$" in k:
            add("warn", "HOWTO V", at(pos), "Math in keywords.")

    # --- floats and captions
    float_envs = ["figure", "figure*", "table", "table*"]
    for env in float_envs:
        pat = re.compile(r"\\begin\{" + re.escape(env) + r"\}(\[[^\]]*\])?(.*?)\\end\{" + re.escape(env) + r"\}", re.S)
        for fm in pat.finditer(t):
            place, body = fm.group(1) or "", fm.group(2)
            base = fm.start(2)
            kind = "table" if env.startswith("table") else "figure"
            caps = list(command_args(body, "caption"))
            if "H" in place or (place and set(place.strip("[]!")) <= set("h")):
                add("info", "HOWTO X", at(fm.start()), f"{env}{place}: IEEE favours top placement ([t]/[!t]).")
            if not caps:
                add("warn", "caption", at(fm.start()), f"{env} without \\caption.")
                continue
            cpos, cap = caps[0]
            abs_c = base + cpos
            words = len(plain(cap).split())
            sents = sentences(cap)
            lab = re.search(r"\\label\{", body)
            if lab and lab.start() < cpos:
                add("check", "HOWTO App. B", at(base + lab.start()), "\\label before \\caption: reference will point to the section number.")
            is_alg = "algorithmic" in body
            content = re.search(r"\\begin\{(tabular\*?|tabularx|IEEEeqnarraybox|threeparttable)\}" if kind == "table" else r"\\includegraphics|\\begin\{(tikzpicture|algorithmic)\}|\\subfloat", body)
            if content:
                if kind == "table" and content.start() < cpos:
                    add("check", "HOWTO X-C", at(abs_c), "Table caption placed after the table; IEEE puts table captions above.")
                if kind == "figure" and content.start() > cpos:
                    add("check", "HOWTO X-A", at(abs_c), "Figure caption placed before the graphic; IEEE puts it below.")
            label = "Algorithm-in-figure" if is_alg else env
            facts.append(f"{label} caption @{at(abs_c)}: {words} words, {len(sents)} sentence(s)")
            capp = plain(cap)
            if re.match(r"(A|An|The)\s", capp):
                add("ref", "ESM captions", at(abs_c), "Caption starts with A/An/The (ESM: 'do not use A, An, or The at the beginning of a figure or table caption').")
            if capp[:1].islower():
                add("ref", "ESM captions", at(abs_c), "Caption does not start with a capital letter.")
            if kind == "table":
                if len(sents) > 1:
                    add("warn", "HOWTO X-C / CT", at(abs_c), f"Table caption has {len(sents)} sentences ({words} words). Table captions 'serve much like titles' (HOWTO); put the explanation in a lettered table note (CT: 'Use letters for table footnotes'; threeparttable). No IEEE source limits caption length as such.")
                if capp.rstrip().endswith("."):
                    add("ref", "ESM captions", at(abs_c), "Table caption ends with a period (ESM: 'does not contain a period at the end of the caption').")
                if len(sents) <= 1 and not looks_title_case(cap):
                    add("info", "HOWTO X-C", at(abs_c), "Table caption is not in title case (HOWTO: usually capitalized like a title).")
                if re.search(r"\d\s*(\\,|~)?\s*(Hz|kHz|MHz|GHz|ms|s|m|mm|cm|km|kg|g|W|V|A|dB|px|K)\b", plain(re.sub(r"\$[^$]*\$", "", cap))) and "\\upshape" not in cap:
                    add("info", "HOWTO X-C", at(abs_c), "Units in a table caption without {\\upshape …}.")

    # --- algorithm floats
    for env in ("algorithm", "algorithm2e"):
        for mm in re.finditer(r"\\begin\{" + env + r"\}", t):
            add("warn", "HOWTO X-B", at(mm.start()), f"\\begin{{{env}}}: IEEE floats are only figures and tables; wrap algorithmic in a figure.")

    # --- figure references in text
    body_start = t.find("\\begin{document}")
    txt = t[body_start:] if body_start >= 0 else t
    off = body_start if body_start >= 0 else 0
    full = [mm for mm in re.finditer(r"\bFigure[~\s]*\\ref", txt)]
    abbr = [mm for mm in re.finditer(r"\bFig\.[~\s]*\\ref", txt)]
    if compsoc and conference and abbr:
        add("info", "HOWTO X-A", at(off + abbr[0].start()), f"'Fig.' used {len(abbr)}× in compsoc conference mode; Computer Society conferences use 'Figure'.")
    if not compsoc and full:
        add("conv", "CT / HOWTO X-A", at(off + full[0].start()), f"'Figure \\ref' used {len(full)}×; IEEE uses 'Fig.' even at the beginning of a sentence (CT, ESM; compsoc conferences excepted).")

    # --- citations
    for mm in re.finditer(r"\\cite\{[^}]*\}\s*,?\s*\\cite\{", txt):
        add("info", "HOWTO VII", at(off + mm.start()), "Adjacent \\cite{}\\cite{}: put them in one \\cite{a,b} so cite.sty can sort/compress.")

    # --- leftovers and centring
    for mm in re.finditer(r"\\centerline\s*\{", t):
        add("info", "HOWTO X-A", at(mm.start()), "\\centerline used; HOWTO recommends \\centering inside the float.")
    if "\\IEEEoverridecommandlockouts" in t and not re.search(r"\\(thanks|IEEEpubid|IEEEPARstart|IEEEmembership)\b", t):
        add("info", "template", rel, "\\IEEEoverridecommandlockouts present but no locked command is used; template leftover.")

    # --- citation order vs reference list order (IEEE numbers references by first citation)
    keys_cited = []
    for mm in re.finditer(r"\\cite\s*(\[[^\]]*\])?\{([^}]*)\}", txt):
        for k in mm.group(2).split(","):
            k = k.strip()
            if k and k not in keys_cited:
                keys_cited.append(k)
    bib_keys = re.findall(r"\\bibitem\s*(?:\[[^\]]*\])?\{([^}]*)\}", t)
    if bib_keys and keys_cited:
        pos = {k: i + 1 for i, k in enumerate(bib_keys)}
        seq = [pos[k] for k in keys_cited if k in pos]
        out = [(i, n) for i, n in enumerate(seq) if n != i + 1]
        if out:
            i, n = out[0]
            add("info", "IEEE reference style", rel, f"References are not numbered in order of first citation (first mismatch: citation #{i + 1} is [{n}]). IEEE style numbers by first citation; IEEEtran.bst does this automatically, a hand-written thebibliography does not.")
        uncited = [k for k in bib_keys if k not in keys_cited]
        if uncited:
            add("info", "bibliography", rel, f"Uncited references: {', '.join(uncited[:8])}.")

    # --- bibliography
    bst = re.search(r"\\bibliographystyle\{([^}]*)\}", t)
    tb = re.search(r"\\begin\{thebibliography\}", t)
    if bst:
        facts.append(f"bibliography: BibTeX style `{bst.group(1)}`")
        if not bst.group(1).startswith("IEEEtran"):
            add("warn", "HOWTO XIII-C", at(bst.start()), f"Bibliography style `{bst.group(1)}`; IEEE papers use IEEEtran.bst.")
    elif tb:
        n = len(re.findall(r"\\bibitem", t))
        facts.append(f"bibliography: thebibliography with {n} \\bibitem")
    else:
        add("info", "HOWTO XIII-C", rel, "No bibliography found.")

    # --- acknowledgments / AI disclosure hints
    ack = re.search(r"\\section\*\{(Acknowledg[^}]*)\}", t)
    if ack:
        facts.append(f"acknowledgment section: `{ack.group(1)}`")
    else:
        facts.append("acknowledgment section: none (check venue rules on AI-use disclosure / funding)")
    check_conventions(t, txt, off, at, rel)
    return t


# ---------------------------------------------------------------- conventions
# Levels: conv = IEEE convention for conferences (CT template, RG, EM, Author Center)
#         ref  = journal-only convention (Editorial Style Manual), reference only
# Keys refer to references/ieee-conventions.md.

ACR_EXEMPT = {"IEEE", "SI", "MKS", "CGS", "AC", "DC", "RMS", "II", "III", "IV", "VI", "VII",
              "VIII", "IX", "XI", "XII", "TABLE", "USA", "UK", "OK", "PDF", "URL", "CPU", "GPU"}
BRITISH = r"\b(colour|behaviour|favour|honour|labour|neighbour|centre|metre|litre|modelling|modelled|labelled|labelling|travelling|analyse|analysed|analysing|optimis\w*|minimis\w*|maximis\w*|normalis\w*|organis\w*|recognis\w*|utilis\w*|characteris\w*|parametris\w*|grey)\b"


def sentence_start(text, pos):
    k = pos - 1
    while k >= 0 and text[k] in " \t~":
        k -= 1
    if k < 0:
        return True
    if text[k] == "\n":
        j = k - 1
        while j >= 0 and text[j] in " \t":
            j -= 1
        if j < 0 or text[j] in "\n.!?}":
            return True
        k = j
    return text[k] in ".!?"


def prose(text):
    """Body text with math, environments that are not prose, and command names blanked
    (lengths preserved so positions stay valid)."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    out = re.sub(r"\\begin\{(equation\*?|align\*?|IEEEeqnarray\*?|eqnarray\*?|tabular\*?|algorithmic|thebibliography)\}.*?\\end\{\1\}", blank, text, flags=re.S)
    out = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]", blank, out, flags=re.S)
    out = re.sub(r"\\(ref|eqref|cite|label|includegraphics|url|href|bibitem|begin|end|usepackage|documentclass)\s*(\[[^\]]*\])?\{[^}]*\}", blank, out)
    out = re.sub(r"\\[A-Za-z]+\*?", lambda m: " " * len(m.group(0)), out)
    return out


def math_spans(text):
    for m in re.finditer(r"\$\$(.*?)\$\$|(?<!\\)\$(.*?)(?<!\\)\$|\\\((.*?)\\\)", text, re.S):
        inline = m.group(1) is None
        yield m.start(), (m.group(1) or m.group(2) or m.group(3) or ""), inline
    for m in re.finditer(r"\\begin\{(equation\*?|align\*?|IEEEeqnarray\*?|gather\*?|multline\*?)\}(.*?)\\end\{\1\}", text, re.S):
        yield m.start(), m.group(2), False


def check_conventions(t, txt, off, at, rel):
    P = prose(txt)

    def A(level, key, pos, msg):
        add(level, key, at(off + pos) if pos is not None else rel, msg)

    # 3. cross-references
    for mm in re.finditer(r"\b(Eqs?\.|[Ee]quations?)\s*~?\s*\(?\\(eq)?ref\b", txt):
        if sentence_start(txt, mm.start()):
            if mm.group(1).startswith("Eq"):
                A("conv", "CT equations", mm.start(), "'Eq.' at sentence start: write 'Equation (1)'.")
        else:
            A("conv", "CT equations", mm.start(), "Write '(1)', not 'Eq. (1)' or 'equation (1)', except at the beginning of a sentence (CT).")
    for mm in re.finditer(r"\b(Ref\.|[Rr]eferences?)\s*~?\s*\\cite\b", txt):
        if not sentence_start(txt, mm.start()):
            A("conv", "CT references", mm.start(), "Write 'in [3]', not 'Ref. [3]' or 'reference [3]', except at the beginning of a sentence (CT).")
    for mm in re.finditer(r"\b[Ss]ubsections?~?\s*\\ref|\bsection~?\s*\\ref", txt):
        A("ref", "ESM sections", mm.start(), "Write 'Section II-A' (capital S); do not use 'Subsection' (ESM).")

    # float placement relative to first citation, and numbering order of first citations
    floats = []
    for fm in re.finditer(r"\\begin\{(figure\*?|table\*?)\}(.*?)\\end\{\1\}", txt, re.S):
        lab = re.search(r"\\label\{([^}]*)\}", fm.group(2))
        if lab:
            floats.append(("table" if fm.group(1).startswith("table") else "figure", fm.start(), lab.group(1)))
    for kind in ("figure", "table"):
        items = [f for f in floats if f[0] == kind]
        firsts = []
        for _, fpos, lab in items:
            r = re.search(r"\\(ref|cref|Cref|autoref)\{[^}]*\b" + re.escape(lab) + r"\b", txt)
            if not r:
                A("conv", "CT figures", fpos, f"{kind} `{lab}` is never referenced in the text.")
                continue
            firsts.append(r.start())
            if r.start() > fpos:
                A("conv", "CT figures", fpos, f"{kind} `{lab}` appears in the source before its first citation (CT: 'Insert figures and tables after they are cited'). Check placement in the PDF.")
        if firsts != sorted(firsts):
            A("ref", "ESM citations", None, f"First citations of {kind}s are not in numerical order (ESM).")

    # 4. title, abstract, headings
    for pos, title in command_args(t, "title"):
        tp = plain(title)
        if ":" in tp or "\\\\" in title and re.search(r"\\\\\s*[a-z]", title):
            add("conv", "CT title", at(pos), "Title has a sub-title (colon). CT: 'Sub-titles are not captured in Xplore and should not be used'.")
        if re.search(r"\\(footnote|thanks)", title):
            add("conv", "CT title", at(pos), "Footnote in title (CT: no footnotes in title or abstract).")
        if re.search(r"\b(new|novel)\b", tp, re.I):
            add("conv", "AC title", at(pos), "'new'/'novel' in title (Author Center: avoid unnecessary words).")
        acr = [w for w in re.findall(r"\b[A-Z][A-Z0-9]*[A-Z]s?\b", tp) if w.rstrip("s") not in ACR_EXEMPT]
        if acr:
            add("conv", "CT abbreviations", at(pos), f"Abbreviations in title: {', '.join(sorted(set(acr)))} (CT: avoid unless unavoidable).")
        break
    for pos, ab in env_blocks(t, "abstract"):
        words = len(plain(ab).split())
        if words > 250:
            add("conv", "AC abstract", at(pos), f"Abstract is {words} words; Author Center: 'a single paragraph up to 250 words' (venue limit wins).")
        if re.search(r"\n\s*\n\s*\S", ab.strip()):
            add("conv", "AC abstract", at(pos), "Abstract has more than one paragraph.")
        if "\\footnote" in ab:
            add("conv", "CT abstract", at(pos), "Footnote in abstract.")
    for mm in re.finditer(r"\\(sub)*section\*?\{\s*(\d+(\.\d+)*|[IVX]+|[A-H])[.)]\s", txt):
        A("conv", "CT headings", mm.start(), "Heading numbered by hand ('Do not number text heads').")
    for mm in re.finditer(r"\\(sub)*section\*?\{([^}]*)\}", txt):
        acr = [w for w in re.findall(r"\b[A-Z][A-Z0-9]*[A-Z]s?\b", mm.group(2)) if w.rstrip("s") not in ACR_EXEMPT]
        if acr:
            A("conv", "CT abbreviations", mm.start(), f"Abbreviation in heading: {', '.join(acr)} (CT: avoid unless unavoidable).")
    sec = [m for m in re.finditer(r"\\(section|subsection)\*?\{", txt)]
    count, cur = {}, None
    for m in sec:
        if m.group(1) == "section":
            cur = m.start(); count[cur] = 0
        elif cur is not None:
            count[cur] += 1
    for spos, n in count.items():
        if n == 1:
            A("conv", "CT headings", spos, "Section has exactly one subsection ('if there are not at least two sub-topics, then no subheads should be introduced').")
    for mm in re.finditer(r"\\section\{\s*Acknowledg", txt):
        A("ref", "ESM acknowledgment", mm.start(), "Acknowledgment heading is numbered; use \\section* (ESM: 'Do not enumerate').")

    # 5. acronyms defined at first use in the body (after the abstract)
    abs_end = txt.find("\\end{abstract}")
    kw_end = txt.find("\\end{IEEEkeywords}")
    body0 = max(abs_end, kw_end, 0)
    first = {}
    for mm in re.finditer(r"(?<![\w\\{])([A-Z][A-Z0-9]*[A-Z])(s?)\b", P[body0:]):
        a = mm.group(1)
        if a in ACR_EXEMPT or a in first:
            continue
        first[a] = body0 + mm.start()
    undefined = []
    for a, pos in first.items():
        before = P[max(0, pos - 2):pos]
        if "(" not in before:
            undefined.append((pos, a))
    if undefined:
        undefined.sort()
        A("conv", "CT abbreviations", undefined[0][0], f"Acronyms whose first use in the body is not '(ACR)' after the spelled-out form: {', '.join(a for _, a in undefined[:15])}{' …' if len(undefined) > 15 else ''}. CT: define at first use in the text, even if defined in the abstract. Verify by eye (false positives: symbols, proper names).")
    for mm in re.finditer(r"\b[A-Z]{2,}'s\b", P):
        A("ref", "ESM acronyms", mm.start(), f"Acronym plural with apostrophe `{mm.group(0)}` (ESM: FETs, not FET's).")
        break

    # 6. numbers and units
    for mm in re.finditer(r"(?<![\w\d.}{=\[\\/-])\.\d+", txt):
        A("conv", "CT units", mm.start(), "Decimal without leading zero: write '0.25', not '.25' (CT).")
        break
    for mm in re.finditer(r"\d\\,\s*(?:\\(?:mathrm|text)\{)?(nm|mm|cm|km|m|s|ms|us|Hz|kHz|MHz|GHz|W|mW|kW|V|mV|A|mA|J|K|dB|dBm|px|ppi|dpi|min|h|kg|g)\b", P):
        A("ref", "ESM units", mm.start(), "Thin space between number and unit; ESM: 'Always use a regular space and not a thin space between numbers and units in text.'")
        break
    for mm in re.finditer(r"\b\d{1,3},\d{3}\b", P):
        A("ref", "ESM numbers", mm.start(), "Comma as thousands separator; ESM uses thin spaces (62 000, but 4000).")
        break

    # 7. words and punctuation
    for pat, key, lvl, msg in [
        (r"\bdata (is|was|has|shows|indicates|suggests)\b", "CT words", "conv", "'data' is plural (CT)."),
        (r"\bet\.\s*al\b|\bet al(?![.\w])", "CT words", "conv", "Write 'et al.' (no period after 'et', period after 'al')."),
        (r"\bnon-[a-z]{3,}", "CT words", "conv", "'non' is joined without a hyphen, usually (CT)."),
        (r"\balternately\b", "CT words", "conv", "'alternatively' is preferred to 'alternately' unless something alternates (CT)."),
        (r"\bessentially\b", "CT words", "conv", "CT: do not use 'essentially' to mean 'approximately' or 'effectively'. Check the meaning."),
        (r"\backnowledgement", "CT acknowledgment", "conv", "Spell 'acknowledgment' without an 'e' after the 'g' (CT, ESM)."),
        (r"\b(i\.e|e\.g)\.(?![,\w])", "ESM punctuation", "ref", "ESM: 'i.e.' and 'e.g.' are followed by a comma."),
        (r"\b(ie|eg)\b(?!\.)", "CT words", "conv", "Write 'i.e.' / 'e.g.'."),
        (BRITISH, "ESM spelling", "ref", "British spelling; ESM: 'Change all British spellings to American spellings.'"),
    ]:
        hits = list(re.finditer(pat, P, re.I if key != "CT words" or "data" in pat else 0))
        if hits:
            words = sorted({h.group(0) for h in hits})
            A(lvl, key, hits[0].start(), f"{msg} Found: {', '.join(words[:6])} ({len(hits)}×).")
    for mm in re.finditer(r"one of us", P, re.I):
        A("conv", "CT acknowledgment", mm.start(), "Avoid 'one of us (R. B. G.) thanks' (CT).")
        break

    # 12. mathematics
    inline_frac = inline_lim = bare_fn = 0
    first_pos = {}
    for mpos, m, inline in math_spans(txt):
        if inline and re.search(r"\\d?frac\b", m):
            inline_frac += 1; first_pos.setdefault("frac", mpos)
        if inline and re.search(r"\\limits|\\displaystyle", m):
            inline_lim += 1; first_pos.setdefault("lim", mpos)
        if re.search(r"(?<![\\A-Za-z])(sin|cos|tan|exp|log|ln|max|min|det|lim|arg|sup|inf|var|cov)(?![A-Za-z])", re.sub(r"\\(text|mathrm|operatorname)\{[^}]*\}", "", m)):
            bare_fn += 1; first_pos.setdefault("fn", mpos)
        if re.search(r"e\^\{[^}]{12,}\}", m):
            A("conv", "EM inline", mpos, "Long exponent on e: use \\exp(...) (EM Rule 4).")
        if re.search(r"\d\s*\\simeq|\\simeq\s*\d", m):
            A("conv", "EM glossary", mpos, "\\simeq next to a number: use \\approx for numerical approximation (EM).")
    if inline_frac:
        A("conv", "EM inline", first_pos["frac"], f"Stacked \\frac in in-line math ({inline_frac}×): use a solidus a/b in text (EM Rule 2).")
    if inline_lim:
        A("conv", "EM inline", first_pos["lim"], f"\\limits or \\displaystyle in in-line math ({inline_lim}×): limits go to the side in text (EM Rule 3).")
    if bare_fn:
        A("conv", "EM roman functions", first_pos["fn"], f"Function name typed as letters in math ({bare_fn}×): use \\sin, \\exp, \\max, \\operatorname{{...}} so it is set in roman (EM §I).")
    for mm in re.finditer(r"\\begin\{eqnarray\*?\}", txt):
        A("conv", "CT LaTeX", mm.start(), "eqnarray: use align or IEEEeqnarray (CT).")
        break
    for mm in re.finditer(r"\\begin\{array\}.*?\\end\{array\}", txt, re.S):
        if "\\nonumber" in mm.group(0):
            A("conv", "CT LaTeX", mm.start(), "\\nonumber inside array (CT: do not).")
    if re.search(r"\\numberwithin\{equation\}|\\renewcommand\s*\{?\\theequation", t):
        add("conv", "EM numbering", rel, "Equation numbering redefined; IEEE numbers equations consecutively through the paper (EM).")

    # 11. reference list (hand-written thebibliography)
    tb = re.search(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", txt, re.S)
    if tb:
        base = tb.start()
        items = list(re.finditer(r"\\bibitem\s*(?:\[[^\]]*\])?\{([^}]*)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", tb.group(0), re.S))
        probs = {}
        def note(key, k, lvl="conv"):
            probs.setdefault((lvl, key), []).append(k)
        for it in items:
            k, body = it.group(1), it.group(2).strip()
            flat = re.sub(r"\s+", " ", body)
            authors = re.split(r"``|“|\\textit|\\emph", flat)[0]
            if re.search(r"\bet al\b", authors):
                named = len([x for x in re.split(r",|\band\b", authors.split("et al")[0]) if x.strip()])
                note("RG et al. (only for more than six authors; name only the first author)" if named > 1 else "RG et al. (check the source has more than six authors)", k)
            names = [x.strip() for x in re.split(r",|\band\b", authors) if x.strip() and "et al" not in x]
            corp = re.compile(r"\b(Ministry|Institute|University|Agency|Organization|Organisation|Society|Association|Commission|Council|Committee|Department|Office|Center|Centre|Inc|Corp|Ltd|Foundation|Group|Laboratory|Bureau|Government|National|World|International)\b")
            if any(re.fullmatch(r"[A-Z][a-z]{2,}(\s+[A-Z][a-z'-]+){1,2}", n) and not corp.search(n) for n in names[:6]):
                note("RG names (given names as initials)", k)
            if not re.search(r"\b(1[89]|20)\d\d\b|n\.d\.", flat):
                note("RG year (every reference needs a year or (n.d.))", k)
            if re.search(r"\bto appear\b", flat, re.I):
                note("RG unpublished (use 'to be published', not 'to appear')", k)
            if re.search(r"\bin press\b", flat, re.I):
                note("CT vs RG ('in press' per CT; RG uses 'to be published')", k, "ref")
            if re.search(r"\b(ibid|op\.\s*cit)\b", flat, re.I):
                note("RG ibid./op. cit. (remove)", k)
            if re.search(r"\b(Proceedings|Conference|International|Symposium|Transactions|Journal)\b", flat):
                note("RG abbreviations (Proc., Conf., Int., Symp., Trans., J.)", k)
            if re.search(r"\b(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|\w+teenth|Twentieth|Thirtieth)\b", flat):
                note("RG ordinals in conference names (1st, not First)", k)
            if re.search(r"\b(in Proc\.|Conf\.|Workshop|Symp\.)", flat) and not re.search(r"\bpp\.|Art\. no\.|\bp\. \d", flat):
                note("RG conference papers have page numbers", k)
            if re.search(r"\bDOI:|https?://(dx\.)?doi\.org/", flat):
                note("RG DOI form ('doi: 10.xxxx/...')", k)
            if re.search(r"Accessed", flat) and not re.search(r"Accessed:?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+\d{1,2},\s+\d{4}", flat):
                note("RG accessed date ('Accessed: Oct. 19, 2026.')", k)
            ends_url = re.search(r"(\\url\{[^}]*\}|https?://\S+)\s*$", flat)
            if not ends_url and not flat.rstrip("} ").endswith("."):
                note("RG final period (all references except those ending with URLs)", k)
            m_t = re.search(r"(``|“)(.*?)(''|”)", flat)
            if m_t:
                tw = re.findall(r"[A-Za-z][\w-]*", m_t.group(2))
                caps = [w for i, w in enumerate(tw[1:], 1) if w[0].isupper() and not w.isupper() and w.lower() not in MINOR and not tw[i - 1].endswith(":")]
                if len(caps) >= 3:
                    note("CT paper titles (capitalize only the first word and proper nouns)", k)
            if "\\footnote" in body:
                note("CT footnote in reference list", k)
        for (lvl, key), ks in probs.items():
            add(lvl, key.split(" (")[0], at(off + base), f"{key}: {', '.join(ks[:8])}{' …' if len(ks) > 8 else ''} ({len(ks)} of {len(items)} items).")
    if re.search(r"\\usepackage(\[(?![^\]]*nocompress)[^\]]*\])?\{[^}]*\bcite\b", t):
        add("ref", "RG citation ranges", rel, "cite.sty compresses citations into ranges '[1]–[4]'; RG (2025) writes them out: '[1], [2], [3], [4]'. HOWTO §VII recommends cite.sty. Preference only.")

    # 13. Xplore / graphics
    if re.search(r"\\usepackage(\[[^\]]*\])?\{[^}]*\bhyperref\b", t):
        add("conv", "AC Xplore", rel, "hyperref loaded: IEEE Xplore PDFs have 'No bookmarks or links'. Becomes a defect if the venue uses PDF eXpress.")
    for mm in re.finditer(r"\\includegraphics\s*(\[[^\]]*\])?\{([^}]*\.(jpe?g|gif|bmp))\}", txt, re.I):
        A("conv", "AC graphics", mm.start(), f"Graphic `{mm.group(2)}`: IEEE accepts PS, EPS, PDF, PNG, or TIFF.")


# ---------------------------------------------------------------- PDF checks

def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def check_pdf(path):
    rel = Path(path).name
    if not shutil.which("pdfinfo"):
        add("info", "pdf", rel, "poppler (pdfinfo/pdffonts/pdfimages) not on PATH; PDF checks skipped.")
        return
    info = run(["pdfinfo", path])
    pages = re.search(r"Pages:\s+(\d+)", info)
    ver = re.search(r"PDF version:\s+([\d.]+)", info)
    if ver:
        facts.append(f"PDF version: {ver.group(1)}")
        if float(ver.group(1)) < 1.4:
            add("conv", "AC Xplore", rel, "PDF version below 1.4 (Xplore requires 1.4 or later).")
    if re.search(r"Encrypted:\s+yes", info):
        add("check", "AC Xplore", rel, "PDF is encrypted/secured (Xplore: no password or security settings).")
    if shutil.which("pdfdetach"):
        att = re.search(r"(\d+) embedded files", run(["pdfdetach", "-list", path]))
        if att and int(att.group(1)) > 0:
            add("conv", "AC Xplore", rel, f"{att.group(1)} embedded file(s) (Xplore: no PDF attachments).")
    size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    if pages:
        facts.append(f"PDF pages: {pages.group(1)}")
    if size:
        w, h = float(size.group(1)), float(size.group(2))
        name = "US letter" if abs(w - 612) < 2 and abs(h - 792) < 2 else ("A4" if abs(w - 595) < 2 and abs(h - 842) < 2 else "other")
        facts.append(f"PDF page size: {w:.0f} x {h:.0f} pt ({name})")
        if name == "other":
            add("check", "HOWTO II-E", rel, "Page size is neither US letter nor A4.")
    fonts = run(["pdffonts", path]).splitlines()[2:]
    t3 = [l for l in fonts if " Type 3 " in l]
    noemb = []
    for l in fonts:
        cols = l.split()
        # columns: name type [encoding...] emb sub uni object ID
        if len(cols) >= 6 and cols[-5] == "no":
            noemb.append(cols[0])
    facts.append(f"PDF fonts: {len(fonts)} entries; not embedded: {len(set(noemb))}; Type 3: {len(t3)}")
    if shutil.which("pdftotext"):
        p1 = run(["pdftotext", "-l", "1", "-layout", path, "-"])
        head = p1.split("Abstract")[0] if "Abstract" in p1 else p1[:3000]
        ords = re.findall(r"\b[1-9](st|nd|rd|th)\s+[A-Z][a-z]", head)
        if ords:
            add("info", "HOWTO IV-B2 / CT", rel + " p1", f"Author names carry ordinal labels ({len(ords)}× '1st/2nd…'): IEEE conference template sample style; HOWTO examples have none. Not wrong; usually removed.")
        lines = [re.sub(r"\s{2,}", " | ", l.strip()) for l in head.splitlines() if l.strip()]
        cells = [c.strip() for l in lines for c in l.split(" | ") if len(c.strip()) > 12 and "@" not in c]
        rep = {c: cells.count(c) for c in set(cells) if cells.count(c) > 1}
        if rep:
            top = max(rep, key=rep.get)
            add("info", "HOWTO IV-B2 / CT", rel + " p1", f"Same author-block line repeated {rep[top]}× on page 1 (e.g. `{top[:60]}`): one column per author, as in the IEEE conference template; HOWTO groups by affiliation instead.")
        if re.search(r"example\.com|Given Name Surname|name of organization|email address or ORCID", head):
            add("check", "placeholder", rel + " p1", "Template placeholder text in the PDF author block.")
    if t3:
        add("check", "HOWTO App. B", rel, f"{len(t3)} Type 3 (bitmap) font(s): " + ", ".join(sorted({l.split()[0] for l in t3}))[:300] + ". IEEE PDF eXpress usually rejects these.")
    if noemb:
        add("check", "HOWTO App. B", rel, "Fonts not embedded: " + ", ".join(sorted(set(noemb)))[:300])
    if shutil.which("pdfimages"):
        low = []
        for l in run(["pdfimages", "-list", path]).splitlines()[2:]:
            c = l.split()
            if len(c) >= 14:
                try:
                    ppi = min(int(c[12]), int(c[13]))
                except ValueError:
                    continue
                if ppi < 300:
                    low.append(f"p{c[0]}:{ppi}ppi")
        if low:
            add("info", "figures", rel, "Raster images under 300 ppi: " + ", ".join(low[:10]) + ". Line art should be vector (HOWTO X-A, App. B).")


def check_log(tex, pdf):
    texp = Path(tex)
    log = texp.with_suffix(".log")
    if pdf and Path(pdf).exists() and Path(pdf).stat().st_mtime < texp.stat().st_mtime - 1:
        add("check", "build", Path(pdf).name, "PDF is older than the .tex: rebuild before judging the PDF.")
    if not log.exists():
        facts.append("LaTeX log: not found")
        return
    L = log.read_text(encoding="latin-1", errors="replace")
    over = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*lines? (\d+)", L)
    undef = re.findall(r"(Reference|Citation) `([^']+)' on page \d+ undefined", L)
    facts.append(f"LaTeX log: overfull hbox={len(over)}, undefined refs/cites={len(undef)}")
    for w, ln in over:
        if float(w) > 1.0:
            add("warn", "HOWTO App. B", f"{texp.name}:{ln}", f"Overfull hbox {w}pt: text/equation runs into the margin.")
    for kind, key in undef[:10]:
        add("check", "build", log.name, f"{kind} `{key}` undefined.")
    if "Rerun to get" in L:
        add("info", "build", log.name, "LaTeX asks for a rerun (cross-references may be stale).")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex")
    ap.add_argument("--pdf")
    a = ap.parse_args()
    if not a.tex and not a.pdf:
        ap.error("give --tex and/or --pdf")
    if a.tex:
        check_tex(a.tex)
        check_log(a.tex, a.pdf)
    if a.pdf:
        check_pdf(a.pdf)
    print("# Mechanical check\n\n## Facts")
    for f in facts:
        print(f"- {f}")
    order = {"check": 0, "warn": 1, "info": 2, "conv": 3, "ref": 4}
    print("\n## Candidates (verify each against the venue rules and references/ieeetran-rules.md)")
    print("level: check = likely defect, warn = deviates from IEEEtran guidance, info = judgement call,")
    print("       conv = IEEE convention (conference template / Reference Guide / math guide / Author Center),")
    print("       ref = journal-only convention (Editorial Style Manual), reference only\n")
    if not findings:
        print("- none")
    for lv, rule, where, msg in sorted(findings, key=lambda x: (order[x[0]], x[2])):
        print(f"- [{lv}] ({rule}) {where} — {msg}")


if __name__ == "__main__":
    sys.exit(main())
