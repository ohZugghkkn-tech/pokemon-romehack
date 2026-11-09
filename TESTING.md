# Prüfungen für dieses Repository

## Reproduzierbare Host-Prüfungen

Voraussetzungen: Python **3.10+** (getestet mit 3.11), Node.js **22**, Git, GNU Make, GCC und G++. Es werden keine ROM, ARM-Toolchain, Emulator-Einstellungen oder GPU benötigt.

Vom Repository-Root aus:

```bash
python3 -m venv .venv
# Linux/macOS; auf Windows eine entsprechende Buildumgebung verwenden.
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/check.py
```

Die Python-Umgebung ist für Entwicklungstests; `requirements-dev.txt` ist keine Behauptung über alle Abhängigkeiten jeder Upstream-Funktion. Nach Einrichtung ist `make check` der gleiche Einstiegspunkt; für ein nicht aktiviertes venv beispielsweise `make PYTHON=.venv/bin/python check`. `make rom` und `make target-tests` sind separate Root-Einstiegspunkte, keine Bestandteile des Host-Runners.

`check.py` bricht bei Fehlern ab und prüft:

1. Syntax aller versionierten und nicht ignorierten neuen JSON-/Python-Dateien, doppelte JSON-Schlüssel, registrierte Karten-/Layoutreferenzen, IDs und Blockdatenlängen. Unveränderte bekannte Abweichungen werden ausdrücklich als offene Schuld gemeldet; neue/geänderte Abweichungen schlagen fehl.
2. Eigene Regressionstests der Prüflogik mit positiven und negativen Fällen.
3. Shader-Hashes, Include-/Preset-Abhängigkeiten, ScaleFX-Passfolge und Parameter.
4. SoulGold-Dokumentationsparser, Websitegenerator, Lernsethelfer und QR-Generator.
5. Die reinen Node-Tests für Party-Export und Versionsvergleich.
6. Die Konsistenz der Musik-Konfiguration.

Vor den Dokumentationstests baut der Runner **nur das Host-Werkzeug `tools/jsonproc/jsonproc`** und erzeugt `include/constants/region_map_sections.h` aus den vorhandenen JSON-/Templatequellen. Dieser Header wird durch `global.h` indirekt benötigt. Beide Ausgaben werden von den vorhandenen Ignore-Regeln ausgeschlossen. Ohne diesen Schritt können die Dokumentationstests auf einem frischen Klon scheitern. Es werden keine Spieldaten für die Website neu veröffentlicht oder ROMs erzeugt.

Die GitHub-Actions-Prüfung liegt unter `.github/workflows/checks.yml`. Die früher mitkopierten Dateien unter `soulgold/.github/workflows/` bleiben historische Upstream-Konfiguration und werden von GitHub hier **nicht** als Workflows ausgeführt. Der Root-Workflow läuft für Pull Requests, Pushes auf `main` und manuell; er hat nur lesende Repository-Berechtigungen und auf volle Commit-IDs fixierte Actions.

Er besitzt getrennte Jobs:

- `host-tests`: führt unseren Host-Runner auf Ubuntu 24.04 mit Python 3.11 und Node 22 aus.
- `target-build-and-tests`: installiert die ARM-/Host-Abhängigkeiten, protokolliert Compilerversionen und führt in `soulgold/` `make -j2 all` sowie `make -j2 check-all` aus. Keine ROMs werden hochgeladen. Die vorhandenen Upstream-Testwerkzeuge werden dabei ausgeführt; ihre Herkunftshinweise bleiben erhalten.

**Der neue Zieljob wurde noch nicht auf GitHub ausgeführt.** Seine Definition ist eine geplante Prüfung, kein Build-Erfolg. Die Distributionstoolchain ist nicht vollständig hermetisch fixiert. Vor Branchschutz/Freigabe den tatsächlichen Lauf prüfen. Dependabot schlägt Action-/Root-Python-Updates per PR vor; es gibt keinen Auto-Merge.

## Separater Browser-Test

`frontier-browser.test.mjs` ist ein Integrationstest, kein reiner Node-Unit-Test. Er benötigt die in `soulgold/package-lock.json` festgelegten npm-Pakete, einen installierten Playwright-Chromium-Browser und einen laufenden HTTP-Server für `soulgold/docs/`.

Beispiel für eine eigene Umgebung mit erlaubtem Browserdownload:

```bash
cd soulgold
npm ci
npx playwright install chromium
python3 -m http.server 8000 --directory docs
```

Danach in einem zweiten Terminal im Verzeichnis `soulgold/`:

```bash
DOCS_TEST_URL=http://127.0.0.1:8000/ node --test tools/soulgold_docs/tests/frontier-browser.test.mjs
```

Der Server ist nur für lokale Tests gedacht. In einer entfernten Vorschauumgebung gelten deren Host-/Port-Vorgaben. Dieser Browser-Test wurde bei der aktuellen Prüfung nicht ausgeführt; der initiale unvorbereitete Sammellauf scheiterte schon am fehlenden Playwright-Paket. Er wird im Host-Runner ausdrücklich nicht als bestanden gezählt.

## ROM- und GPU-Tests bleiben getrennt

Ein bestandener Host-Runner belegt **keine** erfolgreiche ARM-Kompilierung oder Save-Kompatibilität. Für den Spielbuild gelten `soulgold/Makefile`, die Plattformanleitungen und die Hinweise in `ROMHACK-WISSEN.md`. Im Audit fehlten `arm-none-eabi-gcc`, RetroArch und ein Shader-Compiler; deshalb wurden kein ROM-Build, keine C-Zieltests und keine visuelle Shader-Abnahme durchgeführt.

Nie echte eigene Spielstände ohne Backup testen. Keine ROMs, BIOS-Dateien, privaten Saves oder lokale Umgebungen committen.
