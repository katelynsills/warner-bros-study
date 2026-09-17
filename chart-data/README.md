# Data and code for the "citing opinions per year" charts

Warner Bros. Pictures v. Columbia Broadcasting System, 216 F.2d 945 (9th Cir.
1954), against the six later Ninth Circuit opinions on character copyright.

## Files

- `citing-opinions-per-year.csv` — one row per case per year from the year it
  was decided through 2026: citing opinions found in CourtListener, citing
  opinions found outside it, and the total. This is the table the charts draw.
- `citers.csv` — the opinions behind those counts, one row each: the
  CourtListener cluster id, or the external file name (see the companion
  opinion-text bundle for the texts).
- `targets.csv` — the seven cases.
- `known-citers-roster.tsv` — the 56 opinions citing Warner, with where each
  was found and what it cites Warner for.
- `plot_from_csv.py` — rebuilds the chart from the CSV alone. Standard
  library only.
- `build/` — the scripts used in the study. These read the study's opinion
  texts and CourtListener scan output and will not run from this folder
  alone; they are here so the counting can be read.

## How the counts were made

"In CourtListener": one scan over all 10,798,347 opinions in CourtListener's
2026-06-30 bulk export for any citation to the network of cases around
Warner; a citing opinion is a distinct cluster whose text matches the
target's reporter citation (with the spacing and line-number variants seen
in scanned and pleading-paper texts). Opinions CourtListener holds twice
were counted once, and a copy citing its own duplicate was not counted.

"Outside CourtListener": opinions and orders obtained from PACER, the RECAP
Archive, govinfo, the Ninth Circuit's website, and one casebook copy, then
searched for the same citations. These searches were made mainly for Ninth
Circuit courts and mainly for 2015 onward, so they lift the newer cases more
than the older ones. CourtListener holds few unpublished district-court
orders after about 2015.

Counts are raw; nothing is smoothed. Distinct citing opinions, not mentions.

Built 2026-09-15 by `post/exhibits/build_chart_data_bundle.py` in the study repository.
