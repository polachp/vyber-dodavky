#!/usr/bin/env python3
"""Vygeneruje docs/index.html pro GitHub Pages z hlavního srovnání.

Zdroj je srovnani-4-favorite-mobilede.md. První nadpis se nahradí webovým úvodem
(INTRO níže), zbytek dokumentu jde na web beze změny. Šablonu a CSS bere
z build-html.py, aby web vypadal stejně jako lokální HTML.

Použití:
    python3 build-web.py
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "srovnani-4-favorite-mobilede.md"
OUT = HERE / "docs" / "index.html"

INTRO = """# Srovnání favoritů z mobile.de

Vybírám ojetou dodávku jako náhradu za Ford Transit Custom L2H1. Vozí se v ní dvě motorky
s bagáží, párkrát do roka pět lidí a spaní vzadu. Tohle je srovnání čtyř konkrétních nabídek,
mezi kterými se rozhoduju. **Když v tom vidíš něco, co jsem přehlédl, nebo máš s některým
z těch aut zkušenost, ozvi se.**
"""


def load_builder():
    spec = importlib.util.spec_from_file_location("buildhtml", HERE / "build-html.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    bh = load_builder()
    md = SRC.read_text(encoding="utf-8")
    body = md.split("\n", 1)[1].lstrip("\n")   # zahodí původní H1
    page = INTRO + "\n" + body

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{bh.title_of(page, "Výběr dodávky")}</title>
<style>{bh.CSS}</style>
</head>
<body>
<div class="wrap">
{bh.render(page)}
<div class="footer">Generováno z <code>{SRC.name}</code> pomocí <code>build-web.py</code>.
Zdroj i historie jsou v tomhle repozitáři.</div>
</div>
</body>
</html>
""", encoding="utf-8")
    print(f"OK -> {OUT.relative_to(HERE)}  ({OUT.stat().st_size:,} B)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
