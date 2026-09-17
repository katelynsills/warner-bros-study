"""Was Warner ever heavily cited? Small multiples: citing opinions per year
for Warner and for each Ninth Circuit successor on the character question,
all from ONE source (our scan over CourtListener's 10.8M opinions,
../../federal/data/target-citers-2026-09-14.tsv) so the panels are
comparable. Same y-scale on every panel. Distinct citing opinions (clusters).

CourtListener undercounts unpublished district orders after ~2015 for every
one of these cases, so the right-hand ends are all low; the comparison
between panels is what the figure is for.

Output: anchor-comparison.svg (+ dark) and .html with a table view.
"""
import csv, pathlib
from collections import defaultdict
from html import escape as esc

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent.parent / "federal" / "data" / "target-citers-2026-09-14.tsv"
csv.field_size_limit(10**9)

TARGETS = [  # key in the TSV, label, cite
    ("warner-216-f2d-945", "Warner Bros. v. CBS", "216 F.2d 945 (1954)"),
    ("air-pirates-581-f2d-751", "Air Pirates", "581 F.2d 751 (1978)"),
    ("olson-855-f2d-1446", "Olson v. NBC", "855 F.2d 1446 (1988)"),
    ("rice-330-f3d-1170", "Rice v. Fox", "330 F.3d 1170 (2003)"),
    ("halicki-547-f3d-1213", "Halicki v. Sanderson", "547 F.3d 1213 (2008)"),
    ("towle-802-f3d-1012", "DC Comics v. Towle", "802 F.3d 1012 (2015)"),
    ("daniels-958-f3d-767", "Daniels v. Disney", "958 F.3d 767 (2020)"),
]
# CourtListener holds several of these opinions twice, and one copy "cites" the
# other; drop those self-citations.
SELF = {"warner-216-f2d-945": {"235082", "7010462"}, "air-pirates-581-f2d-751": {"358756"},
        "olson-855-f2d-1446": {"511002", "8972023"}, "rice-330-f3d-1170": {"782176", "8437479"},
        "halicki-547-f3d-1213": {"1225530", "3053954"}, "towle-802-f3d-1012": {"2993623", "3004799"},
        "daniels-958-f3d-767": {"4736284", "4751089"}}
seen = defaultdict(dict)  # target -> cluster -> year
for r in csv.DictReader(open(SRC), delimiter="\t"):
    t = r.get("target"); c = r.get("cluster_id", "")
    if c in SELF.get(t, set()): continue
    if t in {k for k, *_ in TARGETS} and c.isdigit() and r.get("year", "").isdigit():
        seen[t][c] = int(r["year"])
per_year = {t: defaultdict(int) for t, *_ in TARGETS}
for t, cl in seen.items():
    for c, y in cl.items(): per_year[t][y] += 1
totals = {t: len(seen[t]) for t, *_ in TARGETS}

# citers found OUTSIDE CourtListener (PACER, RECAP, govinfo, Ninth Circuit CDN,
# casebook): scan every text in ../../opinions/external for each target's cite.
import re, glob
EXT = HERE.parent.parent / "opinions" / "external"
PAT = {
    "warner-216-f2d-945": r"2\s?16\s+(?:\d{1,2}\s+)?F\.?\s*2d\.?\s+(?:\d{1,2}\s+)?945",
    "air-pirates-581-f2d-751": r"581\s+(?:\d{1,2}\s+)?F\.?\s*2d\.?\s+(?:\d{1,2}\s+)?751",
    "olson-855-f2d-1446": r"855\s+(?:\d{1,2}\s+)?F\.?\s*2d\.?\s+(?:\d{1,2}\s+)?1446",
    "rice-330-f3d-1170": r"330\s+(?:\d{1,2}\s+)?F\.?\s*3d\.?\s+(?:\d{1,2}\s+)?1170",
    "halicki-547-f3d-1213": r"547\s+(?:\d{1,2}\s+)?F\.?\s*3d\.?\s+(?:\d{1,2}\s+)?121[34]",
    "towle-802-f3d-1012": r"(?:802|803|902)\s+(?:\d{1,2}\s+)?F\.?\s*3d\.?\s+(?:\d{1,2}\s+)?1012",
    "daniels-958-f3d-767": r"95[28]\s+(?:\d{1,2}\s+)?F\.?\s*3d\.?\s+(?:\d{1,2}\s+)?(?:767|1149)",
}
ext_year = {t: defaultdict(int) for t in PAT}
ext_total = {t: 0 for t in PAT}
# year per file: from the filename, else from INDEX.tsv's date column
import csv as _csv
idx_year = {}
for r in _csv.DictReader(open(EXT / "INDEX.tsv"), delimiter="\t"):
    d = (r.get("date") or "")[:4]
    if d.isdigit():
        idx_year[r["file"]] = int(d); idx_year[r["key"]] = int(d)
for f in sorted(glob.glob(str(EXT / "*.txt"))):
    name = pathlib.Path(f).stem
    # exclude texts that are themselves in CourtListener (fetched copies) and the Leisure Time CL copy
    if "--cl-" in name: continue
    m = re.search(r"(?:^|-)(19\d\d|20\d\d)(?:-|$)", name)
    yr = int(m.group(1)) if m else idx_year.get(name) or idx_year.get(name.split("--")[0])
    if not yr: print("no year for", name); continue
    txt = open(f, errors="replace").read()
    for t, pat in PAT.items():
        if re.search(pat, txt):
            ext_year[t][yr] += 1; ext_total[t] += 1
ymax = max(max(list(per_year[t].values()) + [0]) + 0 for t in per_year)
ymax = max(max((per_year[t].get(y, 0) + ext_year[t].get(y, 0)) for t in per_year for y in range(1954, 2027)), 1)
Y0, Y1 = 1954, 2026
years = list(range(Y0, Y1 + 1))

W = 1100
L, R, T, B = 60, 20, 80, 40
PH, GAP = 70, 26
H = T + len(TARGETS) * (PH + GAP) + B
pw = W - L - R
bw = pw / len(years)

def build(dark=False):
    ink = "#f2f1ec" if dark else "#0b0b0b"; ink2 = "#c3c2b7" if dark else "#52514e"
    line = "#3a3a38" if dark else "#d6d5d0"; surf = "#1a1a19" if dark else "#fcfcfb"
    bar = "#3987e5" if dark else "#2a78d6"; warn = "#d95926" if dark else "#eb6834"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" role="img" aria-label="Citing opinions per year for Warner Bros. v. CBS and six later Ninth Circuit character-copyright opinions, same scale, from one corpus">',
           f'<rect width="{W}" height="{H}" fill="{surf}"/>',
           f'<text x="{L}" y="26" font-size="13" font-weight="700" fill="{ink}">Citing opinions per year, one corpus, same scale <tspan fill="{ink2}" font-weight="400">· CourtListener, 10.8M opinions · distinct citing opinions · hover a bar</tspan></text>']
    lx = L
    out.append(f'<rect x="{lx}" y="36" width="12" height="10" rx="1.5" fill="{bar}"/><text x="{lx+16}" y="45" font-size="11" fill="{ink2}">in CourtListener</text>')
    out.append(f'<rect x="{lx+118}" y="36" width="12" height="10" rx="1.5" fill="{bar}" opacity="0.4"/><text x="{lx+134}" y="45" font-size="11" fill="{ink2}">found outside it (PACER, RECAP, govinfo, court CDN, casebook) — searched mainly for Ninth Circuit courts</text>')
    for pi, (t, label, cite) in enumerate(TARGETS):
        top = T + pi * (PH + GAP); base = top + PH
        col = warn if t.startswith("warner") else bar
        out.append(f'<line x1="{L}" y1="{base}" x2="{W-R}" y2="{base}" stroke="{line}"/>')
        for v in (ymax,):
            y = base - v / ymax * PH
            out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="{line}" stroke-dasharray="2 4"/>')
            out.append(f'<text x="{L-6}" y="{y+4:.1f}" font-size="10" fill="{ink2}" text-anchor="end">{v}</text>')
        out.append(f'<text x="{L-6}" y="{base+4}" font-size="10" fill="{ink2}" text-anchor="end">0</text>')
        out.append(f'<text x="{L}" y="{top-6}" font-size="12" font-weight="700" fill="{ink}">{label} <tspan fill="{ink2}" font-weight="400">{cite} · {totals[t]} in CourtListener{f" + {ext_total[t]} outside" if ext_total[t] else ""}</tspan></text>')
        for i, yr in enumerate(years):
            n = per_year[t].get(yr, 0); m = ext_year[t].get(yr, 0)
            if not n and not m: continue
            h = n / ymax * PH; hm = m / ymax * PH
            if n:
                out.append(f'<rect x="{L+i*bw+1:.1f}" y="{base-h:.1f}" width="{bw-2:.1f}" height="{h:.1f}" rx="1.5" fill="{col}"><title>{esc(label)}, {yr}: {n} in CourtListener</title></rect>')
            if m:
                out.append(f'<rect x="{L+i*bw+1:.1f}" y="{base-h-hm-(2 if n else 0):.1f}" width="{bw-2:.1f}" height="{hm:.1f}" rx="1.5" fill="{col}" opacity="0.4"><title>{esc(label)}, {yr}: {m} found outside CourtListener (PACER, RECAP, govinfo, court CDN)</title></rect>')
        if pi == len(TARGETS) - 1:
            for yr in range(1960, Y1 + 1, 10):
                out.append(f'<text x="{L+(yr-Y0+0.5)*bw:.1f}" y="{base+16}" font-size="11" fill="{ink2}" text-anchor="middle">{yr}</text>')
    out.append('</svg>')
    return "\n".join(out)

svg_l, svg_d = build(False), build(True)
(HERE / "anchor-comparison.svg").write_text(svg_l)
(HERE / "anchor-comparison-dark.svg").write_text(svg_d)
peak = {t: max(per_year[t].items(), key=lambda kv: kv[1]) for t, *_ in TARGETS}
tbl = "\n".join(f"<tr><td>{label}</td><td>{cite}</td><td>{totals[t]}</td><td>{peak[t][1]} in {peak[t][0]}</td></tr>" for t, label, cite in TARGETS)
html = f"""<title>Warner Bros. v. CBS against its successors</title>
<style>
:root{{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--line:#d6d5d0}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1a1a19;--ink:#f2f1ec;--ink2:#c3c2b7;--line:#3a3a38}}}}
:root[data-theme="dark"]{{--bg:#1a1a19;--ink:#f2f1ec;--ink2:#c3c2b7;--line:#3a3a38}}
body{{background:var(--bg);color:var(--ink);padding:24px 16px;max-width:1140px;margin:0 auto;font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
svg{{width:100%;height:auto;display:block}} .light{{display:block}} .dark{{display:none}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .light{{display:none}} :root:not([data-theme="light"]) .dark{{display:block}}}}
:root[data-theme="dark"] .light{{display:none}} :root[data-theme="dark"] .dark{{display:block}}
details{{margin-top:16px;color:var(--ink2)}} table{{border-collapse:collapse;font-size:13px}} td,th{{border-bottom:1px solid var(--line);padding:4px 10px;text-align:left}}
p.sub{{color:var(--ink2)}}
</style>
<div class="light">{svg_l}</div><div class="dark">{svg_d}</div>
<p class="sub">Solid bars are distinct citing opinions found by one scan over CourtListener's corpus, comparable across panels. Lighter segments are citers we found outside it (PACER, RECAP, govinfo, the Ninth Circuit's site, one casebook), which were searched for mainly in Ninth Circuit courts and mainly after 2015, so they lift the recent cases most. CourtListener holds few unpublished district orders after about 2015, so every panel's solid right-hand end is low.</p>
<details><summary>Table view</summary><table><thead><tr><th>Opinion</th><th>Cite</th><th>Citing opinions</th><th>Peak year</th></tr></thead><tbody>{tbl}</tbody></table></details>
<div id="tip" hidden></div>
<style>#tip{{position:fixed;z-index:9;max-width:360px;padding:8px 10px;border-radius:6px;font-size:12px;line-height:1.4;pointer-events:none;background:var(--ink);color:var(--bg);box-shadow:0 2px 8px rgba(0,0,0,.25)}}</style>
<script>
(function(){{
  var tip=document.getElementById('tip');
  document.querySelectorAll('svg *').forEach(function(el){{
    var t=el.querySelector(':scope > title'); if(!t) return;
    var text=t.textContent; t.remove(); el.setAttribute('data-tip',text); el.style.cursor='default';
  }});
  document.addEventListener('mousemove',function(e){{
    var el=e.target.closest&&e.target.closest('[data-tip]');
    if(!el){{tip.hidden=true;return;}}
    tip.textContent=el.getAttribute('data-tip'); tip.hidden=false;
    var x=e.clientX+14,y=e.clientY+14;
    if(x+tip.offsetWidth>window.innerWidth-8) x=e.clientX-tip.offsetWidth-14;
    if(y+tip.offsetHeight>window.innerHeight-8) y=e.clientY-tip.offsetHeight-14;
    tip.style.left=x+'px'; tip.style.top=y+'px';
  }});
}})();
</script>
"""
(HERE / "anchor-comparison.html").write_text(html)
print({label: (totals[t], ext_total[t]) for t, label, _ in TARGETS}, "ymax", ymax)
