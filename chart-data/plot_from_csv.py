"""Rebuild the "citing opinions per year" chart from citing-opinions-per-year.csv.
Usage: python3 plot_from_csv.py   -> writes anchor-lines-calendar.svg next to this file.
No dependencies beyond the standard library."""
import csv, pathlib
from collections import defaultdict
HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "citing-opinions-per-year.csv")))
targets = list(csv.DictReader(open(HERE / "targets.csv")))
data = defaultdict(dict)
for r in rows: data[r["key"]][int(r["year"])] = int(r["total"])
COLORS = {"warner-216-f2d-945": "#eb6834", "air-pirates-581-f2d-751": "#2a78d6", "olson-855-f2d-1446": "#1baf7a",
          "rice-330-f3d-1170": "#eda100", "halicki-547-f3d-1213": "#e87ba4", "towle-802-f3d-1012": "#008300", "daniels-958-f3d-767": "#4a3aa7"}
YMAX = max(v for d in data.values() for v in d.values())

def chart(calendar, path):
    W, H, L, R, T, B = 1100, 460, 50, 215, 50, 50
    pw, ph = W - L - R, H - T - B
    X0, X1 = (1954, 2026) if calendar else (0, 72)
    def X(v): return L + (v - X0) / (X1 - X0) * pw
    def Y(v): return T + ph - v / YMAX * ph
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui,sans-serif"><rect width="{W}" height="{H}" fill="#fcfcfb"/>',
         f'<text x="{L}" y="24" font-size="13" font-weight="700">Citing opinions per year, {"1954–2026" if calendar else "from the year each was decided"}</text>']
    for v in range(0, YMAX + 1, 2):
        o.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W-R}" y2="{Y(v):.1f}" stroke="#d6d5d0"/><text x="{L-8}" y="{Y(v)+4:.1f}" font-size="11" fill="#52514e" text-anchor="end">{v}</text>')
    for v in range(X0 if calendar else 0, X1 + 1, 10):
        if calendar and v % 10: continue
        o.append(f'<text x="{X(v):.1f}" y="{T+ph+18}" font-size="11" fill="#52514e" text-anchor="middle">{v}</text>')
    for j, t in enumerate(targets):
        k = t["key"]; d0 = int(t["decided"]); c = COLORS[k]; w = 3 if k.startswith("warner") else 1.75
        pts = [(y if calendar else y - d0, data[k].get(y, 0)) for y in range(d0, 2027)]
        path_d = " ".join(f"{'M' if i == 0 else 'L'}{X(x):.1f},{Y(v):.1f}" for i, (x, v) in enumerate(pts))
        o.append(f'<path d="{path_d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>')
        y = T + 10 + j * 20; xr = W - R + 16
        o.append(f'<line x1="{xr}" y1="{y}" x2="{xr+18}" y2="{y}" stroke="{c}" stroke-width="{w}"/><text x="{xr+24}" y="{y+4}" font-size="11">{t["label"]} <tspan fill="#52514e">{d0}</tspan></text>')
    o.append("</svg>"); (HERE / path).write_text("\n".join(o)); print("wrote", path)
chart(True, "anchor-lines-calendar.svg")
