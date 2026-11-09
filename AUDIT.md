# Repository-Audit und Korrekturen

Datum: 9. November 2026. Grundlage: Arbeitsbranch `arena/79befa71-pokemon-romehack`.

> **Historischer Erstbefund mit Gegenprüfung:** Die erste Prüfung unten ist kein abschließendes Qualitätsurteil. Der [zweite skeptische Designreview](docs/reviews/2026-11-09-design-review.md) korrigiert ihre schwache Layoutprüfung und ergänzt Ziel-CI, Herkunft und Reviewregeln. Aktuelle Ergebnisse und offene Punkte stehen am Ende dieser Datei.

## Reichweite und Grenzen

Geprüft wurden die Repository-Einbindung, Shaderkette und Abhängigkeiten, die vorhandenen Host-Testfamilien, Dokumentationswerkzeuge, CI-Erreichbarkeit sowie Syntax und Karten-/Layoutreferenzen des versionierten SoulGold-Baums. Das ist eine breite technische Prüfung, **keine vollständige semantische Verifikation aller C-/Assemblerfunktionen oder Sicherheitszertifizierung**.

Die rund 47.000 übernommenen Dateien wurden nicht sämtlich manuell Zeile für Zeile geprüft. Kein ROM-Build, ARM-Testlauf, Browser-Integrationstest oder GPU-Test ist als bestanden zu verstehen. Neue Gameplay-Features wurden nicht umgesetzt.

## Nachgewiesene Befunde und Korrekturen

### 1. Keine aktive CI nach Verzeichnisübernahme

Die mitkopierten Workflows liegen unter `soulgold/.github/workflows/`. GitHub lädt Workflows nur unter `.github/workflows/` des Hauptrepositorys. Deshalb deckten die geerbten Konfigurationen unseren PR-Ablauf nicht ab.

**Korrektur:** neuer lesender Host-Testworkflow im richtigen Root-Pfad, ohne automatische Veröffentlichung von ROMs oder Patches. Die geerbten Workflows wurden nicht blind verschoben: Deren Rootpfade, Branchfilter und Release-Aktionen passen nicht ohne Weiteres zu unserem Projekt.

### 2. Dokumentations-Präprozessor hatte eine Race Condition

`preprocess_source` schrieb jeden Aufruf in dieselbe Datei `/tmp/soulgold_docs_preprocess.c`. Gleichzeitige Aufrufe konnten sich gegenseitig überschreiben; der feste Pfad war zudem nicht portabel und erlaubte Konflikte mit bereits vorhandenen Dateien.

**Korrektur:** GCC erhält den Quelltext über stdin (`-x c -`). Keine gemeinsam beschreibbare temporäre Datei mehr. Neue Tests prüfen parallele Aufrufe mit 32 verschiedenen Eingaben, Fehlerweitergabe sowie stdin-/Include-Argumente.

### 3. Host-Tests auf frischem Klon nicht ausreichend vorbereitet

Der erste Dokumentationstestlauf scheiterte an fehlendem Pillow und dem generierten Header `include/constants/region_map_sections.h`. Der Header wird selbst bei der Dokumentationsvorverarbeitung indirekt über Spielheader eingebunden.

**Korrektur:** `requirements-dev.txt` mit getesteter Pillow-Version, zentraler Runner `scripts/check.py`, explizite Headergenerierung mit dem Host-Werkzeug `jsonproc` und Anleitung in `TESTING.md`. Kein ARM-Compiler und keine ROM nötig für diese Host-Prüfungen.

### 4. Veraltete Text-Erwartung in einem Test

Der Gracidea-Test erwartete „after showing Shaymin“, der Parser verwendete „by showing Shaymin“. Beide beschreiben denselben Erwerb; die Scripts des Goldenrod-Blumenladens enthalten den entsprechenden Shaymin-/Gracidea-Ablauf. Der Fehler war eine veraltete exakte Textassertion, kein nachgewiesener Gameplayfehler.

**Korrektur:** Test auf die vorhandene Formulierung angepasst. Kein Abschwächen der übrigen Itemprüfungen und keine Änderung am Spielscript.

### 5. Browser- und Unit-Tests waren nicht klar getrennt

Ein Sammelaufruf aller `*.test.mjs` versuchte auch einen Browsertest zu starten. Dieser benötigt Playwright, Chromium und einen laufenden Webserver und scheiterte hier am fehlenden Paket.

**Korrektur:** Der Host-Runner wählt die reinen JavaScript-Tests ausdrücklich aus; der Browsertest wird separat mit seinen Voraussetzungen dokumentiert, nicht als bestanden oder still übersprungen gezählt. Keine Änderung an dessen Assertions.

### 6. Unvollständige Installationsanweisung

Ein Beispiel für `make TOOLCHAIN="...` in `soulgold/INSTALL.md` hatte kein schließendes Anführungszeichen.

**Korrektur:** Anführungszeichen ergänzt, damit die Shell nicht auf weitere Eingabe wartet.

### 7. Fehlende Root-Ignore-Regeln und veralteter Projektstatus

Im Hauptrepository fehlten Schutzregeln für lokale Python-Umgebungen, `.env`-Dateien und versehentlich im Root erzeugte ROMs/Saves. Die README behauptete weiterhin, sämtliche SoulGold-Dateien seien unverändert, was nach diesen Werkzeugkorrekturen nicht mehr zutrifft.

**Korrektur:** Root-`.gitignore` ergänzt; README und Wissensdatei mit Teststatus, Korrekturen und klaren verbleibenden Grenzen aktualisiert. Ignore-Regeln ersetzen keinen Secretscanner und schützen keine bereits versionierten Dateien.

## Ausgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Shader-Tests | 5 bestanden; Upstream-Hashes unverändert |
| SoulGold-Dokumentations-Tests | 71 bestanden, einschließlich 3 neuer Präprozessor-Tests |
| Lernsethelfer | 4 bestanden |
| QR-Generator | 4 bestanden |
| JavaScript Party-Export und Versionsvergleich | 32 bestanden |
| Musik-Konfiguration | bestanden; 207 ungenutzte Tracks deaktiviert laut Prüfer |
| Syntax versionierter JSON-/Python-Dateien | keine gefundenen Syntaxfehler; reproduzierbar mit `scripts/check_sources.py` |
| Aktive Karten | 1.103 Einträge; keine fehlende `map.json` |
| Layoutdaten | 1.029 Einträge; keine fehlenden referenzierten Border-/Blockdaten |

Insgesamt **116 bestandene Einzeltests**, zusätzlich Syntax-/Referenz- und Musikprüfungen. Die Zahl prüft nicht die vollständige C-Spielmechanik. Der Runner wurde lokal ausgeführt; ein GitHub-Actions-Ergebnis steht noch aus.

Der initiale Fehlerlauf wurde nicht verschwiegen: Er zeigte fehlende Voraussetzungen, einen abweichenden Itemtext und einen unvorbereiteten Browsertest. Nach Einrichtung und Korrektur wurden die Hostfamilien erneut erfolgreich ausgeführt.

## Offene Risiken / nicht belegt

- **Veröffentlichte ROM vs. Quellstand:** Der Upstream-Hinweis, dass Tag 1.2.1 hinter der veröffentlichten Spielversion liegt, bleibt gültig. Nicht durch Versionszeichenfolgen oder diese Prüfungen lösbar.
- **ARM-Build und Spieltests:** `arm-none-eabi-gcc` fehlt in der aktuellen Umgebung. C-/Assembler-Semantik, Linkerbudget, Bild-/Tonverhalten und Save-Migration sind daher nicht umfassend geprüft.
- **Shaderausführung:** Kein RetroArch-/GPU-Lauf oder Shadercompiler verfügbar. Die Kombination ist statisch geprüft, nicht visuell abgenommen.
- **Browserintegration:** Playwright/Chromium und Server waren nicht vorbereitet; keine visuelle Website-Abnahme.
- **Rechte:** Originalhinweise bleiben erhalten. Der Shader-Header `colorspace-tools.h` ist GPL-2.0-or-later; `stock.slang` und Originalpresets haben keinen eigenen Lizenzvermerk. Keine pauschale rechtliche Freigabe aller übernommenen Spielassets.
- **Starterwunsch:** Mew wurde noch nicht integriert; das ist eine getrennte Featureänderung und kein Bugfix dieses Audits.
- **Keine willkürlichen Massenänderungen:** Kein Engine-Update, keine Neuformatierung der Upstream-Sammlung und keine Änderung gespeicherter IDs oder Save-Strukturen.

Die nächste vertiefte Prüfung sollte ein reproduzierbarer ARM-Baseline-Build mit anschließendem Zieltest- und Save-Testlauf sein. Ein solcher Nachweis darf nicht durch die hier bestandenen Hosttests ersetzt werden.

## Zweite Prüfung: aktueller Stand nach Gegenreview

Verglichen wurden konkrete versionierte Praktiken von pret/pokeemerald, pokeemerald-expansion, Modern Emerald, mGBA und libretro/slang-shaders. Quellen, Momentaufnahme der Sterne und bewusste Nichtübernahmen stehen im [Designreview](docs/reviews/2026-11-09-design-review.md). Popularität ist kein Korrektheitsbeweis.

Neu korrigiert / ergänzt:

- Scanner erfasst jetzt auch neue, nicht ignorierte Dateien, doppelte JSON-Schlüssel, doppelte IDs, ungültige Dimensionen und unbekannte Layoutverweise.
- **26 Layoutgrößenabweichungen entdeckt**, die die erste reine Existenzprüfung übersah. Bytegenau inventarisiert und gegen neue/geänderte Abweichungen abgesichert, **nicht inhaltlich behoben**. Ihre Erreichbarkeit ist offen. Registrierte Karten sind nicht automatisch im Spiel erreichbare Karten.
- 14 eigene Regressionstests für den Scanner; auch die Prüfwerkzeuge werden jetzt geprüft.
- Root-Makefile mit getrennten Host-/ROM-/Zieltest-Einstiegspunkten.
- Zielbuild-/`check-all`-CI ergänzt; Actions auf geprüfte volle Commit-IDs fixiert, Credentials nicht persistiert, Laufzeitlimits und Concurrency ergänzt.
- Herkunftsindex, Liste lokaler Upstream-Eingriffe, Beitragshinweise, PR-Vorlage und separate Release-Checkliste ergänzt.
- Dependabot für Action- und Root-Python-Abhängigkeiten konfiguriert, ohne Auto-Merge.

Erneut lokal ausgeführt:

```text
make PYTHON=/home/user/audit-venv/bin/python check
14 Scanner-Tests + 5 Shader-Tests + 71 Dokumentationstests
+ 4 Lernsettests + 4 QR-Tests + 32 Node-Tests = 130 bestanden
2.974 JSON- und 99 Python-Dateien syntaktisch geprüft
1.103 registrierte Karten / 1.029 Layouts geprüft
26 unveränderte bekannte Größenabweichungen ausdrücklich gemeldet
Musikkonfiguration bestanden
```

Diese Zahlen sind der lokale Stand einschließlich neuer, noch nicht committeter Dateien; sie steigen bei neuen Dateien/Tests. Es sind keine Coverage-Prozente. Der Runner darf für interne Regressionen mit ausdrücklich unveränderter bekannter Schuld grün sein; das ist **keine Freigabe dieser Schuld oder des Spielreleases**.

Zusätzlich wurden Workflow-/Dependabot-YAML lokal geparst und volle Action-IDs sowie lesende Rechte geprüft (PyYAML 6.0.3 in einer externen Audit-Umgebung). Ein Versuch, actionlint aus einem GitHub-Release zu beziehen, scheiterte am in dieser Umgebung nicht erreichbaren Release-Asset-Host. **Kein actionlint-Erfolg und kein GitHub-CI-Erfolg behauptet.**

Weiterhin offen: tatsächlicher ARM-CI-Lauf, Layout-Erreichbarkeits-/Datenkorrekturen, GPU-/Shaderkompilierung, Save- und Browserintegrationstests sowie Rechteklärung. Kein Commit, Push, PR, Merge oder Release wurde in dieser Gegenprüfung vorgenommen.

## Folgeprüfung vom 9. November 2026

Aktueller Stand: [ausgeführte Folgeprüfung und offene Freigaben](docs/reviews/2026-11-09-followup.md). 136 Hosttests, drei Compiler-Helper-Tests, 16 tatsächliche SPIR-V-Kompilierungen und Browserintegration bei drei Breiten erfolgreich. 26 Größenunterschiede geprüft: sieben bestehende Ausschlüsse, neunzehn Überschusspuffer; keine kurzen ausgegebenen Emerald-Puffer. Reale Mapgenerator-Regressionen und Buildschutz ergänzt, keine Kartendaten oder IDs geändert. ARM-Zielergebnis, Saves und GPU-Bildfreigabe bleiben ohne vollständigen Nachweis offen.

**Späterer Nachtrag vom 9. November 2026:** Nach dem Merge von PR #7 war `make -j2 check-all` auf `main` rot (Lauf 42618648812) – 2.260 Tests bestanden, vier Assertions scheiterten (Gigantamax-/Dynamax-Persistenz in diesem Quellstand nicht implementiert; ein reihenfolgeabhängiger Magikarp-Test). Befunde und Behebung: [Nachtrag im Folgeprüfungs-Bericht](docs/reviews/2026-11-09-followup.md#nachtrag-roter-make-check-all-auf-main-nach-dem-pr-7-merge-später-am-9-november-2026).
