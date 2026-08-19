#!/usr/bin/env python3
"""Vygeneruje self-contained HTML ze všech MD souborů v adresáři.

Použití:
    python3 build-html.py            přegeneruje jen zastaralé HTML
    python3 build-html.py --all      přegeneruje všechno
    python3 build-html.py --check    jen vypíše, co je zastaralé (nic nezapisuje)

Vstup:   *.md v adresáři skriptu, kromě souborů v SKIP
Výstup:  stejné jméno s příponou .html
"""
import re
import sys
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent
SKIP = {"CLAUDE.md", "README.md"}

CSS = """
:root{
  --bg:#0f1113; --panel:#16191d; --panel2:#1b1f24; --line:#2a3038;
  --fg:#e6e9ed; --muted:#9aa4b0; --accent:#e8b64c; --accent2:#5aa9e6;
  --good:#5fbf7a; --warn:#e0705a;
}
@media (prefers-color-scheme: light){
  :root{
    --bg:#f6f7f9; --panel:#ffffff; --panel2:#f0f2f5; --line:#dde1e7;
    --fg:#1a1d21; --muted:#5c6672; --accent:#b8860b; --accent2:#1d6fb8;
    --good:#237a3d; --warn:#b53d26;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; padding:0 20px 80px;
  background:var(--bg); color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:31px;line-height:1.2;margin:40px 0 6px;letter-spacing:-.02em}
h2{font-size:23px;margin:44px 0 14px;padding-bottom:9px;border-bottom:2px solid var(--line);letter-spacing:-.01em}
h3{font-size:18px;margin:30px 0 10px;color:var(--accent)}
p{margin:12px 0}
a{color:var(--accent2);text-decoration:none;border-bottom:1px solid transparent}
a:hover{border-bottom-color:currentColor}
strong{color:var(--fg);font-weight:650}
em{color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:40px 0}
ol,ul{padding-left:22px}
li{margin:7px 0}
code{background:var(--panel2);padding:2px 6px;border-radius:4px;font-size:.88em}

.tablewrap{overflow-x:auto;margin:18px 0;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{padding:10px 13px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
thead th{
  background:var(--panel2);font-weight:650;font-size:12.5px;
  text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
  white-space:nowrap;position:sticky;top:0;z-index:1
}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--panel2)}
/* krátké buňky (čísla, data, ceny) se nezalamují */
td.nb{white-space:nowrap}
tr.pick{background:rgba(232,182,76,.09)}
tr.pick:hover{background:rgba(232,182,76,.15)}
tr.pick td:nth-child(3){font-weight:650}

.meta{color:var(--muted);font-size:14.5px}
.legend{
  display:inline-block;margin:14px 0 0;padding:9px 14px;
  background:var(--panel);border:1px solid var(--line);border-radius:8px;font-size:14px
}
.footer{margin-top:56px;padding-top:18px;border-top:1px solid var(--line);
  color:var(--muted);font-size:13px}
@media(max-width:640px){
  body{padding:0 12px 60px} h1{font-size:25px} h2{font-size:20px}
  table{font-size:13px} th,td{padding:8px 9px}
}
"""


def title_of(md_text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def render(md_text: str) -> str:
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "attr_list", "sane_lists"],
    )

    # tabulky do scrollovacího kontejneru
    html_body = html_body.replace("<table>", '<div class="tablewrap"><table>')
    html_body = html_body.replace("</table>", "</table></div>")

    # krátké buňky označit jako nezalomitelné (čísla, data, ceny, „bez nehody")
    def nowrap_cell(m):
        inner = m.group(1)
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        return f'<td class="nb">{inner}</td>' if len(plain) <= 26 else m.group(0)

    html_body = re.sub(r"<td>(.*?)</td>", nowrap_cell, html_body, flags=re.S)

    # zvýraznění řádků s hvězdičkou v prvním sloupci
    def mark(m):
        row = m.group(0)
        first = re.search(r"<td>(.*?)</td>", row, re.S)
        if first and "★" in first.group(1):
            return row.replace("<tr>", '<tr class="pick">', 1)
        return row

    html_body = re.sub(r"<tr>.*?</tr>", mark, html_body, flags=re.S)

    # vysvětlivky do rámečku
    html_body = html_body.replace(
        "<p><strong>Vysvětlivky:</strong>",
        '<p class="legend"><strong>Vysvětlivky:</strong>',
    )
    return html_body


def build_one(src: pathlib.Path) -> pathlib.Path:
    dst = src.with_suffix(".html")
    md_text = src.read_text(encoding="utf-8")
    out = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_of(md_text, src.stem)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{render(md_text)}
<div class="footer">Vygenerováno z <code>{src.name}</code> pomocí <code>build-html.py</code>.
Změny dělej v MD a spusť build znovu.</div>
</div>
</body>
</html>
"""
    dst.write_text(out, encoding="utf-8")
    return dst


def sources():
    return sorted(p for p in HERE.glob("*.md") if p.name not in SKIP)


def is_stale(src: pathlib.Path) -> bool:
    dst = src.with_suffix(".html")
    return not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime


def main() -> int:
    args = set(sys.argv[1:])
    check = "--check" in args
    force = "--all" in args

    todo = [s for s in sources() if force or is_stale(s)]

    if check:
        if todo:
            print("Zastaralé HTML:")
            for s in todo:
                print(f"  {s.name} -> {s.with_suffix('.html').name}")
            return 1
        print("Všechno HTML je aktuální.")
        return 0

    if not todo:
        print("Nic k přegenerování. (--all vynutí všechno)")
        return 0

    for s in todo:
        dst = build_one(s)
        print(f"OK -> {dst.name}  ({dst.stat().st_size:,} B)")

    # osiřelá HTML bez zdrojového MD
    stems = {s.stem for s in sources()}
    orphans = [
        h for h in sorted(HERE.glob("*.html"))
        if h.stem not in stems
    ]
    if orphans:
        print("\nPozor, HTML bez zdrojového MD (kandidáti na smazání):")
        for h in orphans:
            print(f"  {h.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
