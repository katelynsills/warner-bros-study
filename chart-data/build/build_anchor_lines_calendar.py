"""Citations per CALENDAR year (objective time): Warner and its Ninth Circuit successors
on one chart, on one calendar axis, 1954–2026.

y = citing opinions in that year, from EVERY source we hold (CourtListener
scan + PACER/RECAP/govinfo/court CDN/casebook texts in opinions/external),
raw yearly counts. x = calendar year. Each line starts the year its opinion was decided.

Reuses the counting in build_anchor_comparison.py.
"""
import pathlib, runpy
from collections import defaultdict
from html import escape as esc

HERE = pathlib.Path(__file__).resolve().parent
ns = runpy.run_path(str(HERE / "build_anchor_comparison.py"))
TARGETS, per_year, ext_year = ns["TARGETS"], ns["per_year"], ns["ext_year"]
DECIDED = {"warner-216-f2d-945": 1954, "air-pirates-581-f2d-751": 1978, "olson-855-f2d-1446": 1988,
           "rice-330-f3d-1170": 2003, "halicki-547-f3d-1213": 2008, "towle-802-f3d-1012": 2015, "daniels-958-f3d-767": 2020}
HORIZON = 2026
COLORS = {  # validated 7-hue categorical, light/dark
    "warner-216-f2d-945": ("#eb6834", "#d95926"),
    "air-pirates-581-f2d-751": ("#2a78d6", "#3987e5"),
    "olson-855-f2d-1446": ("#1baf7a", "#199e70"),
    "rice-330-f3d-1170": ("#eda100", "#c98500"),
    "halicki-547-f3d-1213": ("#e87ba4", "#d55181"),
    "towle-802-f3d-1012": ("#008300", "#008300"),
    "daniels-958-f3d-767": ("#4a3aa7", "#9085e9"),
}
WIN = 1  # raw yearly counts (no smoothing)

Y0 = 1954
series = {}
for t, label, cite in TARGETS:
    y0 = DECIDED[t]
    raw = [per_year[t].get(y, 0) + ext_year[t].get(y, 0) for y in range(y0, HORIZON + 1)]
    sm = []
    for i in range(len(raw)):
        lo, hi = max(0, i - WIN // 2), min(len(raw), i + WIN // 2 + 1)
        sm.append(sum(raw[lo:hi]) / (hi - lo))
    series[t] = (raw, sm)
XMAX = HORIZON - Y0
YMAX = max(max(s) for _, s in series.values())

W, H = 1100, 460
L, R, T, B = 50, 70, 50, 50
pw, ph = W - L - R, H - T - B
def X(i): return L + i / XMAX * pw  # i = calendar year - Y0
def Y(v): return T + ph - v / YMAX * ph

def build(dark=False):
    ink = "#f2f1ec" if dark else "#0b0b0b"; ink2 = "#c3c2b7" if dark else "#52514e"
    line = "#3a3a38" if dark else "#d6d5d0"; surf = "#1a1a19" if dark else "#fcfcfb"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" role="img" aria-label="Citing opinions per calendar year, Warner Bros. v. CBS against six later Ninth Circuit opinions, raw yearly counts">',
           f'<rect width="{W}" height="{H}" fill="{surf}"/>',
           f'<text x="{L}" y="24" font-size="13" font-weight="700" fill="{ink}">Citing opinions per year, 1954–2026</text>']
    for v in range(0, int(YMAX) + 1, 2):
        out.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W-R}" y2="{Y(v):.1f}" stroke="{line}" stroke-width="{1.5 if v==0 else 1}"/>')
        out.append(f'<text x="{L-8}" y="{Y(v)+4:.1f}" font-size="11" fill="{ink2}" text-anchor="end">{v}</text>')
    for yr in range(1960, HORIZON + 1, 10):
        i = yr - Y0
        out.append(f'<line x1="{X(i):.1f}" y1="{T}" x2="{X(i):.1f}" y2="{T+ph}" stroke="{line}" stroke-dasharray="2 4"/>')
        out.append(f'<text x="{X(i):.1f}" y="{T+ph+18}" font-size="11" fill="{ink2}" text-anchor="middle">{yr}</text>')
    # muted successors first, Warner on top
    order = [t for t, *_ in TARGETS if not t.startswith("warner")] + ["warner-216-f2d-945"]
    labels = {t: (lab, cite) for t, lab, cite in TARGETS}
    ends = []
    for t in order:
        raw, sm = series[t]
        c = COLORS[t][1 if dark else 0]
        w_ = 3 if t.startswith("warner") else 1.75
        off = DECIDED[t] - Y0
        d = " ".join(f"{'M' if i==0 else 'L'}{X(i+off):.1f},{Y(v):.1f}" for i, v in enumerate(sm))
        lab, cite = labels[t]
        total = sum(raw)
        out.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w_}" stroke-linejoin="round" stroke-linecap="round"><title>{esc(lab)}, {cite}: {total} citing opinions over {len(raw)-1} years; peak {max(raw)} in {DECIDED[t]+raw.index(max(raw))}</title></path>')
        ends.append((Y(sm[-1]), X(len(sm) - 1 + off), c, lab, DECIDED[t], t.startswith("warner")))
    # direct labels: at each line's peak, or the next-best local high point with open room
    placed = []  # (x0, y0, x1, y1) boxes already used
    def free(box): return all(box[2] < b[0] or box[0] > b[2] or box[3] < b[1] or box[1] > b[3] for b in placed)
    for t, lab, cite in TARGETS:
        raw, sm = series[t]; c = COLORS[t][1 if dark else 0]
        off = (DECIDED[t] - Y0) if "Y0" in globals() else 0
        text = f"{lab} {DECIDED[t]}"; tw = 6.4 * len(text) + 4
        cands = sorted(range(len(sm)), key=lambda i: (-sm[i], i))  # highest first
        for i in cands:
            px, py = X(i + off), Y(sm[i])
            for dy in (-10, -24, 14, 28, -38, 42):
                y = py + dy
                x0 = min(max(px - tw / 2, L), W - R - tw)
                box = (x0, y - 11, x0 + tw, y + 3)
                if free(box) and T < y - 11 and y + 3 < T + ph + 2:
                    placed.append(box)
                    out.append(f'<text x="{x0 + tw/2:.1f}" y="{y:.1f}" font-size="11" font-weight="{"700" if t.startswith("warner") else "600"}" fill="{c}" text-anchor="middle" stroke="{surf}" stroke-width="3" paint-order="stroke">{esc(text)}</text>')
                    break
            else: continue
            break
    out.append('</svg>')
    return "\n".join(out)

svg_l, svg_d = build(False), build(True)
(HERE / "anchor-lines-calendar.svg").write_text(svg_l)
(HERE / "anchor-lines-calendar-dark.svg").write_text(svg_d)
rows = "\n".join(f"<tr><td>{lab}</td><td>{cite}</td><td>{DECIDED[t]}</td><td>{sum(series[t][0])}</td><td>{max(series[t][0])} in {DECIDED[t]+series[t][0].index(max(series[t][0]))}</td><td>{sum(series[t][0][:11])}</td></tr>" for t, lab, cite in TARGETS)
tip = (HERE / "anchor-comparison.html").read_text().split('<div id="tip" hidden></div>', 1)[1]
html = f"""<title>Warner Bros. v. CBS and its successors, by year</title>
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
<p class="sub">Calendar time. Each line starts the year its opinion was decided. Counts are distinct citing opinions per year. The searches outside CourtListener were aimed mainly at Ninth Circuit courts after 2015, which lifts the newer cases more than the old ones.</p>
<details><summary>Table view</summary><table><thead><tr><th>Opinion</th><th>Cite</th><th>Decided</th><th>Citing opinions</th><th>Peak year</th><th>First 10 years</th></tr></thead><tbody>{rows}</tbody></table></details>
<div id="tip" hidden></div>{tip}"""
(HERE / "anchor-lines-calendar.html").write_text(html)
print({lab: (sum(series[t][0]), sum(series[t][0][:11])) for t, lab, _ in TARGETS})
