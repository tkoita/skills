# IEEEtran rules, quoted

Source: Michael Shell, *How to Use the IEEEtran LaTeX Class* (IEEEtran_HOWTO.pdf, 28 pp.),
https://mirror.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran_HOWTO.pdf
Section numbers below are the HOWTO's own. Quote these when reporting, and say "HOWTO §X" so the
reader can look it up. If something is not in this file, do not present it as an IEEEtran rule —
fetch the HOWTO or the venue's instructions and quote them instead.

Contents
1. Precedence — whose rule wins
2. Class options (§II)
3. Title and authors (§IV-A, §IV-B)
4. Abstract and index terms (§V)
5. Citations and bibliography (§VII, §XIII-C)
6. Figures, algorithms, tables (§X)
7. Production problems (Appendix B)
8. The other IEEE template (conference_101719.tex)
9. Things that are NOT IEEEtran rules

---

## 1. Precedence

1. The venue's author instructions / CFP / author kit (page limits, paper size, blind review,
   copyright notice, PDF eXpress, AI disclosure …). These override everything below.
2. The template the venue distributes, if it names one.
3. IEEEtran_HOWTO (this file).
4. IEEE Editorial Style Manual (spelling of units, reference formats) — cite it only after
   fetching it; it is not summarised here.

The HOWTO itself defers to venues repeatedly ("unless told otherwise", "Unless specifically
instructed otherwise … by the conference"). A deviation from the HOWTO is a *recommendation*
finding, not a violation, unless the venue adopts the HOWTO or its template.

## 2. Class options (§II)

- §II-A: "10pt is used by the vast majority of papers. Notable exceptions are technote papers,
  which use 9pt text and the initial submissions to some conferences that use 11pt."
- §II-B: draft, draftcls, draftclsnofoot give double spacing and 1-inch margins — not camera-ready.
- §II-C1 Conference mode: margins increased, text height ≈ 9.25in, extra bottom clearance.
  "Headings and page numbers are not displayed in the headers or footers."
  "The \author text is placed within a tabular environment to allow for multicolumn formatting
  of author names and affiliations." "The figure captions are centered."
  "The following commands are intentionally disabled: \thanks, \IEEEPARstart, \IEEEbiography,
  \IEEEbiographynophoto, \IEEEpubid, \IEEEpubidadjcol, \IEEEmembership, and
  \IEEEaftertitletext. If needed, they can be reenabled by issuing the command:
  \IEEEoverridecommandlockouts."
  "When using conference mode, most users will also want to equalize the columns on the last
  page (see Section XIV)."
- §II-D1a: "Unless specifically instructed otherwise by the conference that is being submitting
  to, do not invoke the comsoc option with conference papers."
- §II-D2a: compsoc conference mode keeps Arabic section numbering. "Be aware that many IEEE
  Computer Society conferences use the traditional conference format and compsoc mode should not
  be used with them."
- §II-E: "Since the IEEE primarily uses US letter, authors should usually select the
  letterpaper option before submitting their work to the IEEE—unless told otherwise (typically
  by conferences held outside the United States)." "authors should ensure that all
  post-processing (PS, PDF, etc.) uses the same paper specification as the .tex document.
  Problems here are by far the number one reason for incorrect margins."
- §II-G: "Since the IEEE always uses two column text, the onecolumn option is of interest only
  with draft papers."

## 3. Title and authors

### §IV-A Paper title
"Titles are generally capitalized except for words such as a, an, and, as, at, but, by, for, in,
nor, of, on, or, the, to and up, which are usually not capitalized unless they are the first or
last word of the title. Line breaks (\\) may be used to equalize the length of the title lines.
Do not use math or other special symbols in the title."

### §IV-B2 Names in conference mode (verbatim, the passage most often misread)
"For papers with three or less affiliations, a multicolumn format is preferred:"

```latex
\author{\IEEEauthorblockN{Michael Shell}
\IEEEauthorblockA{School of Electrical and\\
Computer Engineering\\
Georgia Institute of Technology\\
Atlanta, Georgia 30332--0250\\
Email: mshell@ece.gatech.edu}
\and
\IEEEauthorblockN{Homer Simpson}
\IEEEauthorblockA{Twentieth Century Fox\\
Springfield, USA\\
Email: homer@thesimpsons.com}
\and
\IEEEauthorblockN{James Kirk\\
and Montgomery Scott}
\IEEEauthorblockA{Starfleet Academy\\
San Francisco, California 96678-2391\\
Telephone: (800) 555--1212\\
Fax: (888) 555--1212}}
```

"Use \and to separate the affiliation columns. The columns will automatically be centered with
respect to each other and the side margins."

"If there are more than three authors and/or the text is too wide to fit across the page, use
an alternate long format:"

```latex
\author{\IEEEauthorblockN{Michael Shell\IEEEauthorrefmark{1},
Homer Simpson\IEEEauthorrefmark{2},
James Kirk\IEEEauthorrefmark{3},
Montgomery Scott\IEEEauthorrefmark{3} and
Eldon Tyrell\IEEEauthorrefmark{4}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}School of Electrical and Computer Engineering\\
Georgia Institute of Technology, Atlanta, Georgia 30332--0250\\
Email: mshell@ece.gatech.edu}
\IEEEauthorblockA{\IEEEauthorrefmark{2}Twentieth Century Fox, Springfield, USA\\
Email: homer@thesimpsons.com}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Starfleet Academy, San Francisco, California 96678-2391\\
Telephone: (800) 555--1212, Fax: (888) 555--1212}
\IEEEauthorblockA{\IEEEauthorrefmark{4}Tyrell Inc., 123 Replicant Street, Los Angeles, California 90210--4321}}
```

"The \IEEEauthorrefmark{} command will generate a footnote symbol corresponding to the number in
its argument. Use this to link the author names to their respective affiliations."

§IV-B4: "Names in compsoc conference mode are done in the same way as traditional conference mode."

How to read it (this is where earlier analyses went wrong):
- Columns are per **affiliation**, not per author. The multicolumn example itself has four
  authors; Kirk and Scott share one column because they share Starfleet Academy.
- The two criteria use different nouns: "three or less **affiliations**" → multicolumn
  preferred; "more than three **authors** and/or too wide" → long format. With four authors and
  one or two affiliations, both are defensible; do not call either one wrong.
- If every author has the same affiliation, the closest HOWTO form is one block: all names in
  one \IEEEauthorblockN, the affiliation once in one \IEEEauthorblockA, no refmarks.
- Repeating the same affiliation in several columns, or numbering authors "1st, 2nd …", comes
  from conference_101719.tex (section 8), not from the HOWTO.
- IEEE's own conference template says the opposite of the HOWTO on grouping: "Names should not
  be listed in columns nor group by affiliation. Please keep your affiliations as succinct as
  possible (for example, do not differentiate among departments of the same organization)."
  (ieee-conventions.md §9). For a conference paper, neither layout is wrong; say which IEEE
  source each one matches instead of calling one of them a deviation.

§IV-C: "Conference papers do not have running headings, so \markboth{}{} has no effect when in
conference mode. Authors should not put any name information in the headings (if used) of
anonymous peer review papers."
§IV-D: "Publication IDs are not to be placed by the author on camera ready conference papers so
\IEEEpubid{} is disabled in conference mode."

## 4. Abstract and index terms (§V)

"Math, special symbols and/or citations should generally not be used in abstracts."
Keywords go in \begin{IEEEkeywords} … \end{IEEEkeywords} (printed as "Index Terms").
"Do not use math or special symbols in the keywords."
The HOWTO describes keywords for journal and technote papers; whether a conference wants them is
the venue's call.

## 5. Citations and bibliography

§VII: "IEEEtran will produce citation numbers that are individually bracketed in IEEE style.
('[1], [5]' as opposed to the more common '[1, 5]' form.)" With \usepackage{cite} "the
adjacent citation numbers will automatically be sorted and compressed (ranged) IEEE style. (Of
course, multiple adjacent citations should always all be declared within a single \cite, comma
separated, for this to work.)" Compsoc sorts but does not compress: \usepackage[nocompress]{cite}.

§XIII-B: acknowledgments via \section*{Acknowledgment}; "IEEE Computer Society papers typically
use the plural form 'Acknowledgments'."

§XIII-C: "Bibliographies are most easily (and correctly) generated using the IEEEtran BIBTEX
package … \bibliographystyle{IEEEtran} \bibliography{IEEEabrv,mybibfile}". When sending .tex to
others, paste the .bbl into a thebibliography environment.

§XIV: "Balancing the last two columns is especially important for camera ready work." Use
\newpage or \enlargethispage{-X.Yin} on the last page, or \IEEEtriggeratref{n}.

## 6. Figures, algorithms, tables (§X)

§X (placement): "most IEEE journals strongly favor the positioning of floats to the top of the
page and rarely, if ever, use bottom floats … IEEE journals never place floats in the first
column of the first page … Middle in-text placement ('here') is usually not used for IEEE work
with one notable exception—IEEE Computer Society conferences."

§X-A Figures: "(1) figures should be centered via the LaTeX \centering command … (2) the
caption follows the graphic; and (3) any labels must be declared after (or within) the caption
command." "When referring to figures in typical IEEE papers, authors should use the abbreviation
'Fig.', but in IEEE Computer Society conference papers they should use the full word 'Figure'."
Vector (EPS/PDF) for drawings and graphs; bitmaps for photos.
The HOWTO sets no length limit for figure captions, and IEEE's style manual shows multi-sentence
figure captions as normal (ieee-conventions.md §8).

§X-A1 Subfigures: subfigure.sty "not recommended for new work". Load subfig with
caption=false: `\usepackage[caption=false,font=footnotesize]{subfig}`. subcaption.sty "can not
be recommended at this time because it does not provide an option to prevent the underlying
caption.sty from taking control of main caption formatting away from IEEEtran." "most IEEE
authors/journals do not employ subfigure captions, but instead reference/describe all of the
subfigures (a), (b), etc., within the main caption."

§X-B Algorithms: "IEEE publications use the figure environment to contain algorithms … do not
use the floating algorithm environment of algorithm.sty … or algorithm2e.sty … as the only
floating structures IEEE uses are figures and tables."

§X-C Tables: "the IEEE places table captions before the tables and, given that they serve much
like titles, are usually capitalized except for words such as a, an, and, as, at, but, by, for,
in, nor, of, on, or, the, to and up, which are usually not capitalized unless they are the first
or last word of the caption."
"to prevent a change of meaning that would result from case changes, the IEEE generally uses the
standard text font, not the small caps font, when rendering units as well as letters in math in
table captions. This can be achieved via the use of \upshape:"
`\caption{… (FLB) = 10 {\upshape Hz}; 75% Load; 1450 {\upshape r/min})}`
Table text is \footnotesize by default; IEEE "often uses tables with 'open sides'".
§X-C1: notes under a table — enclose tabular in a minipage, or use threeparttable ("A very good
approach for handling footnotes within tables (including those that float)").
Practical consequence: IEEEtran prints table captions centered in small caps, so a
multi-sentence explanatory caption becomes a block of small caps. Recommend a short title-like
caption plus a lettered note under the table. No IEEE source sets a caption length; see
ieee-conventions.md §8 before saying anything about length.

§X-D: figure*/table* span both columns; they cannot go at the bottom without stfloats.

## 7. Production problems (Appendix B)

- "Placing labels before captions: This is considered to be one of the most frequent mistakes
  made in LaTeX of all time."
- "Authors should allow IEEEtran to manage the fonts. Unless specifically instructed otherwise …
  do not attempt to use packages that override the default fonts such as pslatex, mathptm, etc."
- "Authors should not attempt to manually alter the margins, paper size (except as provided in
  IEEEtran class options) or use packages that do so (geometry.sty, etc.). There should be no
  need to add spacing around figures, equations, etc."
- Line art as vector; photos EPS/PDF, PNG or TIFF. "The use of other graphic formats such as BMP,
  EMF, VSD, etc., is unacceptable for IEEE journals." "Some IEEE conferences may be more liberal."
- "ensure that only vector (Type 1) fonts are being used and that all fonts are embedded and
  subsetted. A document that uses bitmapped fonts and/or fails to contain all (and only) the
  needed font glyphs may be rejected by the IEEE."
- Use graphicx only (no psfig, epsf). Long equations must be broken to fit the column.
- "Papers with problems such as incorrect margins, font types, PDF format errors and/or improper
  font embedding can incur delays during the manuscript acceptance process."

## 8. The other IEEE template (conference_101719.tex)

IEEE also distributes a Word/LaTeX "conference template" (file conference_101719.tex in the
IEEE Manuscript Templates for Conference Proceedings). It is a legitimate IEEE template, but it
is not the HOWTO and its author block differs:

- one column per author, labelled `1\textsuperscript{st} Given Name Surname`, `2nd …`;
- placeholder affiliation lines `dept. name of organization (of Aff.)`, `name of organization
  (of Aff.)`, `City, Country`, `email address or ORCID`;
- a `\thanks{Identify applicable funding agency here. If none, delete this.}`;
- body text that is itself guidance, including a warning that template text must be removed
  before submission.

Report leftover placeholder/guidance text as a defect (the template itself warns that "Failure
to remove the template text from your paper may result in your paper not being published.").
The ordinal labels are a sample artefact, usually removed. One column per author follows the
template's own guidance ("Names should not be listed in columns nor group by affiliation"), so it
is not a deviation for a conference paper. The template's writing guidance is collected in
ieee-conventions.md.

## 9. Things that are NOT IEEEtran rules (or IEEE conventions)

Do not report these as IEEE rules unless the venue states them:
- a maximum caption length for figures or tables (no IEEE source sets one — checked HOWTO, the
  conference template, the Editorial Style Manual and the Author Center graphics pages);
- a required number of keywords;
- a required abstract length (venues often set one — check);
- page limits (always venue-specific);
- whether author names must be in a particular order or style beyond the above.
- "Published by CPS / IEEE Computer Society, so use 'Figure' and compsoc": CPS publishes many
  conferences in the plain conference format. Use 'Figure' and the compsoc option only when the
  venue (or its CPS Author Kit) says the paper is in Computer Society format (HOWTO §II-D2a warns
  that many Computer Society conferences use the traditional format).
- Reference numbering by order of first citation is IEEE reference style (IEEE Reference Guide),
  not an IEEEtran_HOWTO rule; IEEEtran.bst produces it automatically. Report it as C unless you
  have fetched and quoted the guide.
