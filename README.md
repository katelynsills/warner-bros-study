# Warner Bros. v. CBS: data behind "Indicators of Silently Overruled Cases"

Data and code for the blog post
[Indicators of Silently Overruled Cases](https://katelynsills.com/law/indicators-of-silently-overruled-cases/)
(Kate Sills, September 2026), a small case study of *Warner Bros. Pictures v.
Columbia Broadcasting System*, 216 F.2d 945 (9th Cir. 1954), the "Sam Spade"
case, and the six later Ninth Circuit opinions on copyright in characters.

## What is here

- **`chart-data/`**: the table and code behind the post's "citing opinions per
  year" chart. One row per case per year, the opinions behind each count, the
  roster of the 56 opinions citing Warner, a standard-library Python script that
  redraws the chart from the CSV alone, and the scripts used in the study.
  See [`chart-data/README.md`](chart-data/README.md) for how the counts were made.
- **The opinions** (release asset, not in the tree):
  [`warner-opinions-5994.tar.gz`](https://github.com/katelynsills/warner-bros-study/releases/latest)
  holds the text of every opinion read for the study, 5,994 files as UTF-8
  plain text, with a `manifest.csv` (path, source, CourtListener ids, case
  name, court, date, citations, provenance) and a README on how the text was
  made and what it may be used for. 69 MB compressed, 224 MB unpacked.

## Sources and credit

Court opinions are public records. Most of the texts come from the Free Law
Project's [CourtListener](https://www.courtlistener.com/) bulk data and API;
please credit Free Law Project if you reuse them. The rest were pulled from
PACER, the RECAP Archive, govinfo, the Ninth Circuit's website, and one
casebook copy on H2O. Details are in the README inside the tarball.

Corrections welcome as issues on this repository.
