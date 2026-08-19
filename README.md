# Výběr dodávky

Podklady k výběru ojeté dodávky jako náhrady za Ford Transit Custom L2H1.
Srovnání čtyř konkrétních nabídek z mobile.de: dva Fordy Transit/Tourneo Custom,
VW T6 Mixto a Renault Trafic.

**Web: https://polachp.github.io/vyber-dodavky/**

Repozitář: https://github.com/polachp/vyber-dodavky

## Co je kde

| Soubor | K čemu |
|---|---|
| `srovnani-4-favorite-mobilede.md` | hlavní dokument, zdroj pravdy. Detaily z inzerátů, závěr, další krok, rozměry, vyřazené vozy |
| `srovnani-4-favorite-mobilede.html` | totéž ke čtení lokálně v prohlížeči |
| `docs/index.html` | verze pro web, publikuje ji GitHub Pages ze složky `docs` |
| `build-html.py` | generuje HTML ze všech MD v kořeni |
| `build-web.py` | generuje `docs/index.html` z hlavního MD, nahradí první nadpis úvodem pro čtenáře |
| `publish.bat` | build obou HTML plus commit a push, jedním příkazem |

HTML se needituje ručně, vždy se přegeneruje z MD.

## Po každé změně

Ve Windows stačí spustit:

```
publish.bat "popis zmeny"
```

Skript přegeneruje obě HTML, commitne a pushne. GitHub Pages se aktualizují samy
do minuty nebo dvou.

Ručně je to totéž ve čtyřech krocích:

```
pip install markdown      # jen poprvé
python build-html.py      # lokální HTML
python build-web.py       # docs/index.html pro web
git add -A && git commit -m "popis" && git push
```

## Poznámka ke stránce

Náhledy fotek a odkazy míří přímo na mobile.de. Až prodejci inzeráty stáhnou,
obrázky i odkazy přestanou fungovat.
