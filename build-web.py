#!/usr/bin/env python3
"""Vygeneruje obsah složky docs pro GitHub Pages.

Hlavní dokument (srovnani-4-favorite-mobilede.md) se stane docs/index.html, jeho první
nadpis nahradí webový úvod (INTRO níže). Ostatní MD v kořeni (detaily jednotlivých vozů)
se vygenerují vedle jako docs/<jmeno>.html, takže odkazy mezi nimi fungují i na webu.

Šablonu a CSS bere z build-html.py, aby web vypadal stejně jako lokální HTML.

Použití:
    python3 build-web.py
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).parent
DOCS = HERE / "docs"
MAIN = HERE / "srovnani-4-favorite-mobilede.md"
SKIP = {"CLAUDE.md", "README.md"}

INTRO = """# Srovnání favoritů

Vybírám ojetou dodávku jako náhradu za Ford Transit Custom L2H1. Vozí se v ní dvě motorky
s bagáží, párkrát do roka pět lidí a spaní vzadu. Tohle je srovnání konkrétních nabídek,
mezi kterými se rozhoduju. **Když v tom vidíš něco, co jsem přehlédl, nebo máš s některým
z těch aut zkušenost, ozvi se.**
"""


def load_builder():
    spec = importlib.util.spec_from_file_location("buildhtml", HERE / "build-html.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def page(bh, md_text: str, source_name: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{bh.title_of(md_text, "Výběr dodávky")}</title>
<style>{bh.CSS}</style>
</head>
<body>
<div class="wrap">
{bh.render(md_text)}
<div class="footer">Generováno z <code>{source_name}</code> pomocí <code>build-web.py</code>.
Zdroj i historie jsou v tomhle repozitáři.</div>
</div>
</body>
</html>
"""


def main() -> int:
    bh = load_builder()
    DOCS.mkdir(exist_ok=True)

    md = MAIN.read_text(encoding="utf-8")
    body = md.split("\n", 1)[1].lstrip("\n")      # zahodí původní H1
    out = DOCS / "index.html"
    out.write_text(page(bh, INTRO + "\n" + body, MAIN.name), encoding="utf-8")
    print(f"OK -> docs/{out.name}  ({out.stat().st_size:,} B)")

    for src in sorted(HERE.glob("*.md")):
        if src.name in SKIP or src == MAIN:
            continue
        dst = DOCS / (src.stem + ".html")
        dst.write_text(page(bh, src.read_text(encoding="utf-8"), src.name), encoding="utf-8")
        print(f"OK -> docs/{dst.name}  ({dst.stat().st_size:,} B)")

    orphans = [
        h for h in sorted(DOCS.glob("*.html"))
        if h.name != "index.html" and not (HERE / (h.stem + ".md")).exists()
    ]
    if orphans:
        print("\nPozor, HTML v docs bez zdrojového MD (kandidáti na smazání):")
        for h in orphans:
            print(f"  docs/{h.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
