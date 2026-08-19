@echo off
REM Pregeneruje HTML a publikuje web na GitHub Pages.
REM Pouziti:  publish.bat "popis zmeny"
setlocal
cd /d "%~dp0"

set "MSG=%~1"
if "%MSG%"=="" set "MSG=Aktualizace srovnani"

echo [1/5] Kontrola baliku markdown...
python -c "import markdown" 2>nul
if errorlevel 1 (
  echo     chybi, instaluji...
  python -m pip install markdown
  python -c "import markdown" 2>nul
  if errorlevel 1 goto :errmd
)

echo [2/5] Lokalni HTML...
python build-html.py
if errorlevel 1 goto :err

echo [3/5] Web do docs...
python build-web.py
if errorlevel 1 goto :err

echo [4/5] Commit...
git add -A
git commit -m "%MSG%"

echo [5/5] Push...
git push
if errorlevel 1 goto :errpush

echo.
echo Hotovo. Web: https://polachp.github.io/vyber-dodavky/
echo Zmena naskoci do minuty nebo dvou.
goto :end

:errmd
echo.
echo Balik markdown se nepodarilo nainstalovat. Nic se necommitovalo.
echo Zkus rucne:  python -m pip install markdown
goto :end

:err
echo.
echo CHYBA pri generovani HTML. Nic se necommitovalo.
goto :end

:errpush
echo.
echo CHYBA pri push. Zkontroluj prihlaseni ke GitHubu.

:end
endlocal
pause
