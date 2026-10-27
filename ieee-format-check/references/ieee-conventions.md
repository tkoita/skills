# IEEE conventions, quoted

`ieeetran-rules.md` covers rules (the venue's instructions and IEEEtran_HOWTO). This file covers
**conventions**: how IEEE papers are usually written, according to IEEE's own style documents. A
departure from a convention is never category A, and is category C or D only (see SKILL.md).
Every quote below was checked against the source text on 2026-10-19.

Contents
1. Sources and how much weight each carries
2. Decisions where IEEE sources disagree
3. Cross-references in text (figures, equations, sections, citations)
4. Title, abstract, index terms, headings
5. Abbreviations and acronyms
6. Numbers and units
7. Words and punctuation
8. Captions (figures and tables) — no length convention exists
9. Authors and affiliations
10. Acknowledgment
11. Reference list
12. Mathematics
13. IEEE Xplore PDF and graphics

---

## 1. Sources

| Key | Document | Version | Scope | Weight |
|---|---|---|---|---|
| CT | IEEE conference template, LaTeX (`conference_101719.tex` / `.pdf`; IEEE "Manuscript Templates for Conference Proceedings") | PDF built 2019-10-17 | Conference papers. The body text is itself guidance. | Strong (category C) |
| RG | IEEE Reference Guide | V 3.28.2025 | All IEEE publications | Strong for references (C) |
| EM | IEEE "Editing Mathematics" (IEEE Mathematics Style Guide for Authors) | V 10.27.2023 | All IEEE publications | Strong for math (C) |
| ESM | IEEE Editorial Style Manual for Authors | undated Google Doc | "general writing guidelines for IEEE Transactions, Journals, and Letters" | Reference only for conferences (D) |
| AC | IEEE Author Center, conference pages (structure, Xplore requirements, graphics) | read 2026-10-19 | Conference papers | Strong (C); Xplore items can become A if the venue uses PDF eXpress |

URLs:
- RG: https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf
- EM: https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/Editing-Mathematics.pdf
- ESM: https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/ieee-editorial-style-manual/
- CT: https://www.ieee.org/conferences/publishing/templates.html
- AC: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/ (structure-your-paper,
  meet-ieee-xplore-requirements, improve-your-graphics)

## 2. Decisions where IEEE sources disagree

| Issue | What the sources say | Decision for this skill |
|---|---|---|
| Author block | HOWTO §IV-B2: one column per affiliation. CT: "Names should not be listed in columns nor group by affiliation." | Conference paper: CT's layout is the convention, HOWTO's is also acceptable. Report neither as wrong; mention which source each matches. |
| "et al." in the reference list | RG: list up to six names; "If there are more than six names listed, use the primary author's name followed by 'et al.'" CT: "Unless there are six authors or more give all authors' names" | Follow RG (newer, all IEEE): et al. only for seven or more authors. |
| Accepted / submitted papers | RG: "to be published" / "submitted for publication", never "to appear in". CT: "in press" / "unpublished". | Follow RG. Flag "to appear"; mention "in press" only as D. |
| Citation ranges | RG: "Reference ranges in text will not include an en dash. All references will be written out." HOWTO §VII: cite.sty compresses ranges "IEEE style". | Mention as D (preference) only. |
| Punctuation after equations | EM: "the only punctuation used at the end of an equation is a period." CT: "Punctuate equations with commas or periods when they are part of a sentence" | Follow CT for conferences: comma or period as the sentence needs. |
| Type size in figures | CT: "Use 8 point Times New Roman for Figure labels." AC: "Type should appear approximately 9-10 point when viewed at full size." | Report only if clearly smaller than 8 pt or inconsistent; quote both. |

## 3. Cross-references in text

- Figures. CT: "Use the abbreviation 'Fig. 1', even at the beginning of a sentence." ESM: "The
  abbreviation is used even when it begins a sentence." (Exception: compsoc conference mode uses
  "Figure"; HOWTO §X-A.)
- Equations. CT: "Use '(1)', not 'Eq. (1)' or 'equation (1)', except at the beginning of a
  sentence: 'Equation (1) is . . .'"
- Citations. CT: "Refer simply to the reference number, as in [3]—do not use 'Ref. [3]' or
  'reference [3]' except at the beginning of a sentence: 'Reference [3] was the first . . .'"
  CT: "The sentence punctuation follows the bracket [2]." RG: references "appear on the line, in
  square brackets, inside the punctuation." RG: "Use 'et al.' when three or more names are given
  for a reference cited in the text."
- Sections (ESM, D): "Capitalize the word 'Section.' Do not use the word 'Subsection'; use
  'Section' and write out the complete citation."
- Citing part of a source (ESM, D): write "[1, Fig. 2]", "[1, eq. (8)]", not "in Fig. 2 of
  reference [1]".
- Floats. CT: "Insert figures and tables after they are cited in the text." ESM: "All first
  citations of figures and tables in the article must be in numerical order."

## 4. Title, abstract, index terms, headings

- CT title note: "Sub-titles are not captured in Xplore and should not be used".
- CT abstract: "CRITICAL: Do Not Use Symbols, Special Characters, Footnotes, or Math in Paper
  Title or Abstract."
- AC (Structure Your Paper): title should be "specific, concise, and descriptive"; "Avoid using
  unnecessary words such as 'new' or 'novel'." Abstract: "a single paragraph up to 250 words";
  "self-contained with no abbreviations, footnotes, references, or mathematical equations".
- ESM (D): "Abstract, must be one paragraph and between 150 to 250 words." "Index Terms appear in
  alphabetical order … Capitalize the first word of the Index Terms list; lowercase the rest
  unless capitalized in text."
- CT headings: "Do not number text heads—LaTeX will do that for you." "if there are not at least
  two sub-topics, then no subheads should be introduced."
- Venue limits on abstract length override all of the above.

## 5. Abbreviations and acronyms

- CT: "Define abbreviations and acronyms the first time they are used in the text, even after
  they have been defined in the abstract. Abbreviations such as IEEE, SI, MKS, CGS, ac, dc, and
  rms do not have to be defined. Do not use abbreviations in the title or heads unless they are
  unavoidable."
- ESM (D): plural without apostrophe — "FET (singular); FETs (plural)."

## 6. Numbers and units

- CT: "Use a zero before decimal points: '0.25', not '.25'." ESM agrees: "Always add a zero
  before decimals".
- CT: "Use either SI (MKS) or CGS as primary units. (SI units are encouraged.)" "Avoid combining
  SI and CGS units". "Do not mix complete spellings and abbreviations of units". "Spell out units
  when they appear in text: '. . . a few henries', not '. . . a few H'."
- ESM (D): "spell out numbers below 11, and use numerals for others unless they begin a sentence
  or are combined in a phrase". "Always use a regular space and not a thin space between numbers
  and units in text." "Use thin spaces instead of commas between numbers in tens or hundreds of
  thousands (e.g., 62 000, 100 000, but 4000)."

## 7. Words and punctuation (CT "Some Common Mistakes" unless marked)

- "The word 'data' is plural, not singular."
- "There is no period after the 'et' in the Latin abbreviation 'et al.'."
- "The prefix 'non' is not a word; it should be joined to the word it modifies, usually without a
  hyphen."
- "A graph within a graph is an 'inset', not an 'insert'. The word alternatively is preferred to
  the word 'alternately' (unless you really mean something that alternates)."
- "Do not use the word 'essentially' to mean 'approximately' or 'effectively'."
- Homophones: affect/effect, complement/compliment, discreet/discrete, principal/principle;
  "Do not confuse 'imply' and 'infer'."
- "The abbreviation 'i.e.' means 'that is', and the abbreviation 'e.g.' means 'for example'."
- Quotation marks: periods and commas go inside only "when a complete thought or name is cited";
  "A parenthetical phrase or statement at the end of a sentence is punctuated outside of the
  closing parenthesis (like this)."
- ESM (D): "Change all British spellings to American spellings." "The abbreviations etc., i.e.,
  and e.g., are parenthetic and use the comma". "In a series of three or more terms, use a comma
  immediately before the coordinating conjunction".

## 8. Captions — no length convention exists

No IEEE source sets a length for figure or table captions or asks for them to be short or concise
(checked: HOWTO, CT, ESM, AC graphics pages). Do not report caption length as a problem in
itself. What the sources do say:

Tables
- HOWTO §X-C: table captions "serve much like titles" (title case).
- ESM (D): "The descriptive text of the table caption does not contain a period at the end of the
  caption, although punctuation may be necessary within the caption itself. In general, table
  captions should be set as an inverted pyramid." Example: "TABLE I / Parameter Values".
- Explanations belong in table notes: CT "Use letters for table footnotes." (its sample table has
  note "a"); HOWTO §X-C1 recommends threeparttable.
- So: a multi-sentence table caption → suggest a title-like caption plus a lettered note.

Figures
- Figure captions may be descriptive and several sentences long. ESM example: "Fig. 3. Output
  resistance as a function of channel doping for 1-m-long gate. (a) InGaAs and (b) InP JFETs with
  pinchoff voltage as a parameter." ESM: "Figure footnotes should be placed as part of the
  caption."
- ESM (D): "The first word of the caption should always be capitalized". "In general, do not use
  A, An, or The at the beginning of a figure or table caption." Sub-figure labels: "the citation
  of (a), (b), etc., should always appear before the corresponding caption part."
- CT axis labels: "Use words rather than symbols or abbreviations when writing Figure axis labels"
  ("Magnetization, M", not "M"); "If including units in the label, present them within
  parentheses. Do not label axes only with units." "write 'Temperature (K)', not
  'Temperature/K'."
- CT: "Figure captions should be below the figures; table heads should appear above the tables."
  "Place figures and tables at the top and bottom of columns. Avoid placing them in the middle of
  columns."

## 9. Authors and affiliations (CT)

"Author names should be listed starting from left to right and then moving down to the next line.
This is the author sequence that will be used in future citations and by indexing services. Names
should not be listed in columns nor group by affiliation. Please keep your affiliations as
succinct as possible (for example, do not differentiate among departments of the same
organization)." See §2 for how this sits next to HOWTO §IV-B2.

## 10. Acknowledgment

- CT: "The preferred spelling of the word 'acknowledgment' in America is without an 'e' after the
  'g'." "Avoid the stilted expression 'one of us (R. B. G.) thanks . . .'." "Put sponsor
  acknowledgments in the unnumbered footnote on the first page."
- ESM (D): "Do not enumerate the Acknowledgment heading." "Write the Acknowledgment section in the
  third person."
- ESM: AI-generated content "shall be disclosed in the acknowledgments section of any article
  submitted to an IEEE publication" (venues such as CANDAR adopt this as a rule — then it is A).

## 11. Reference list (RG unless marked)

- Names: "the given name of the author or editor is abbreviated to the initial only and precedes
  the last name." "IEEE publications must list names of all authors, up to six names. If there are
  more than six names listed, use the primary author's name followed by 'et al.'"
- "All references must include a date that comprises at least the year of publication … If no
  date is provided, use the abbreviation '(n.d.)'".
- "Do not combine references. There must be only one reference with each number." ESM: "Use of
  one reference number to designate a group of references is not permitted."
- "All references, except those ending with URLs, will end with a period, including those with a
  DOI."
- "Check the reference list for 'ibid.' or 'op. cit.' … should be eliminated".
- Conference names: "Write out all the remaining words, but omit most articles and prepositions
  like 'of the' and 'on.' That is, Proceedings of the 1996 Robotics and Automation Conference
  becomes Proc. 1996 Robot. Automat. Conf." "If an ordinal number is in the conference name, use
  the numerical form instead of spelling it out (e.g., '1st' instead of 'First')." "NOTE: All
  published conference or proceedings papers have page numbers."
- Basic conference format: J. K. Author, "Title of paper," in *Abbreviated Name of Conf.*,
  (location optional), year, pp. xxx–xxx, doi: xxx.
- Not yet published: "to be published" when accepted, "submitted for publication" when not;
  "do not use 'to appear in.'"
- Online: "The style of the accessed date is 'Accessed: Abbrev. month and day, year.'"; order is
  "Accessed date. DOI. [Online]. Available: URL" with no period after a URL. DOI form in the
  examples: "doi: 10.1109/…."
- CT: "Capitalize only the first word in a paper title, except for proper nouns and element
  symbols." CT: "Do not put footnotes in the abstract or reference list."
- Numbering by order of first citation: CT says "number citations consecutively"; IEEEtran.bst
  does it automatically. No IEEE source found that states "order of first citation" in those
  words — report as C with that caveat.

## 12. Mathematics (EM unless marked)

- "I. Functions and Operators Always Set in Roman Font" (sin, cos, exp, log, ln, max, min, det,
  lim, Pr …). "Thin spaces occur on either side of both functions and differentials." In LaTeX:
  use \sin, \exp, \max, \operatorname.
- In-line math: "Rule 2: Fractions should not appear stacked in line." "Rule 3: Collective signs
  should not appear with limits to top and bottom, but to the side instead." "Rule 4: Use Roman
  function exp instead of e followed by a lengthy superscript."
- "Equations within an article are numbered consecutively from the beginning of the article to the
  end." (Section-based numbering only in some Transactions.) "Hyphens and periods are usually
  removed from equation numbers, i.e., (1a) rather than (1-a)".
- ≈ (\approx) "to indicate approximation between numbers"; ≃ (\simeq) for "asymptotic equivalence
  between functions".
- CT: "Italicize Roman symbols for quantities and variables, but not Greek symbols." "Use a long
  dash rather than a hyphen for a minus sign." "Be sure that the symbols in your equation have been
  defined before or immediately following the equation." "Please don't use the {eqnarray}
  equation environment. Use {align} or {IEEEeqnarray} instead." "Do not use \nonumber inside the
  {array} environment."

## 13. IEEE Xplore PDF and graphics (AC)

Meet IEEE Xplore Requirements (what PDF eXpress checks):
- "The PDF is version 1.4 (Acrobat 5) or later, but not Acrobat 9, X, or XI."; "All fonts are embedded or subset."; "No password
  or other security settings are included."; "No bookmarks or links are included."; "There are no
  crop marks, registration marks, date stamps, timestamps, or any other mark"; "No PDF attachments
  are included."
- "Please note that not all conferences use IEEE PDF eXpress." If the venue uses it, these become
  category A.
Improve Your Graphics:
- "IEEE accepts PS, EPS, PDF, PNG, or TIFF formats for graphics submission."
- "Most graphics are published at one column width (3.5 inches / 21 picas wide)" "or two column
  width (7.16 inches / 43 picas wide)."
- "either convert all text to outlines or embed the fonts." "Typefaces and type sizes should be
  consistent in all your graphics and tables."
- "Evaluate your graphs by checking whether they can be interpreted correctly from a greyscale
  printout."
- "IEEE will no longer accept submitted papers which include the 'Lena image.'"
Finalize Your Paper: "Make sure that default text from the paper template is removed." "Check the
title and all author names for accuracy."
