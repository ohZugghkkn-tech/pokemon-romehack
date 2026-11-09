# KI → KI: Roadmap bis zum fertigen SoulGold-Spielupdate

Stand: **9. November 2026 (UTC)**. Arbeitsbranch: `arena/1137d45d-pokemon-romehack`. Merge Request: [PR #7](https://github.com/ohZugghkkn-tech/pokemon-romehack/pull/7). **Nicht selbst mergen: Der Nutzer übernimmt den Merge.**

## 1. Kurzantwort: Wie weit sind wir?

**Etwa 55 % des unten definierten Wegs zu einem eigenen, getesteten Spielupdate.** Das ist eine gewichtete Projektplanung, keine Messung der Spielqualität, kein Anteil geprüfter Codezeilen und kein Beweis, dass das Spiel zu 55 % spielbar ist. SoulGold wurde als bestehendes Spiel übernommen; wir entwickeln es nicht von null. Der noch offene Aufwand für Spieltests und Save-Kompatibilität kann die Schätzung deutlich verändern.

**Technische Grundlage weitgehend vorhanden; eigenes Gameplayupdate und Release noch nicht fertig.** Kein Engine-Versionssprung beschlossen oder durchgeführt. „Update“ bezeichnet hier die eigene Änderung auf dem übernommenen Quellstand einschließlich Prüfung und späterer Patch-Veröffentlichung.

| Phase vom Start bis zur Freigabe | Gewicht | Stand | Beitrag zum Gesamtstand |
|---|---:|---:|---:|
| 1. SoulGold-Quellen direkt übernehmen, Herkunft sichern | 10 % | 100 % | 10,00 Punkte |
| 2. Ziel, Grenzen und technische Ausgangslage klären | 10 % | 80 % | 8,00 Punkte |
| 3. Hosttests, Fehlerkorrekturen und Layoutschutz | 15 % | 100 % | 15,00 Punkte |
| 4. Bestehende Shader importieren und technisch prüfen | 10 % | 80 % | 8,00 Punkte |
| 5. Dokumentationswebsite im Browser prüfen | 10 % | 100 % | 10,00 Punkte |
| 6. ARM-ROM bauen und vollständige Zieltests bestehen | 15 % | 25 % | 3,75 Punkte |
| 7. Vorgemerkten Mew-Startertausch umsetzen und testen | 5 % | 0 % | 0,00 Punkte |
| 8. Save-Kompatibilität nachweisen | 10 % | 0 % | 0,00 Punkte |
| 9. Spielabläufe und Regressionen im Spiel prüfen | 10 % | 0 % | 0,00 Punkte |
| 10. Versioniertes Update als rechtlich geprüftes Patchpaket freigeben | 5 % | 0 % | 0,00 Punkte |
| **Summe** | **100 %** | | **54,75 ≈ 55 %** |

Berechnung: Summe aus `Gewicht × Phasenstand / 100`. Prozente sind Meilensteinschätzungen, keine Zeitschätzung. Ein grüner Build würde Phase 6 voranbringen, aber nicht automatisch Saves oder Spielabläufe freigeben. 100 % in einer Phase bedeutet ausschließlich Erfüllung ihres hier begrenzten Umfangs.

## 2. Verbindlicher Kontext für die nächste KI

- **SoulGold für GBA auf Emerald-Basis**, nicht DS-SoulSilver. Basis laut importiertem README: pokeemerald-expansion 1.15.0.
- Direkte Dateien in `soulgold/`, **keine Submodule**. Upstream-Tag 1.2.1, Commit `e73803309e78231142160b3e1029df884bc8b5f1`; Herkunft in `UPSTREAM.json` und `ROMHACK-WISSEN.md`.
- Upstream warnt, dass der Quellstand hinter dem veröffentlichten Spiel liegt. Tag/Versionsanzeige sind **kein Nachweis der Gleichheit zur offiziellen ROM**.
- Shader sind fertige importierte Algorithmen: **ScaleFX → Bevel → Image Adjustment**. Keine neuen Shader erfinden; Upstreamdateien, Hashes und Lizenzhinweise erhalten.
- **Keine Emulator-Konfiguration** ins Projekt aufnehmen: keine Treiberauswahl, Auflösung, Vollbild- oder Seitenverhältniseinstellung. Interne Shader-Passskalierung ist erlaubt.
- Mew darf einen beliebigen der neun Starter ersetzen; noch nicht umgesetzt. Kein Auftrag zu weiteren Gameplayfeatures oder einem umfassenden Engineupgrade ableiten.
- Keine privaten Saves, BIOS oder ROMs committen oder als CI-Artefakte hochladen. Keine Merge-Aktion ohne neue ausdrückliche Erlaubnis.
- Auf dem bestehenden Arena-Branch bleiben. Für Git lokal `git`, für PR/CI `gh` verwenden. Keine Zugangsdaten anfordern.

## 3. Nachgewiesener Stand und Werkzeuge

### [x] Phase 1 – Quellimport und Herkunft: 100 %

**Womit:** Git, direkte Upstream-Dateiübernahme, Herkunftsmanifest, Lizenz-/Credithinweise.

- Quellen vollständig im Hauptrepository eingebunden, keine Submodule.
- Shaderdateien separat mit fixiertem Upstreamstand und Hashprüfung importiert.
- Einschränkung zur offiziellen Release-ROM dokumentiert.

**Nachlesen:** `UPSTREAM.json`, `ROMHACK-WISSEN.md`, `docs/upstream-changes.md`, `shaders/README.md`.

### [ ] Phase 2 – Zieldefinition: 80 %

**Womit:** Anforderungsabgleich mit Nutzer, Quellen-/Releasevergleich und MD-Dokumentation.

- [x] Plattform, Importmodus, Shaderkette und verbotene Emulator-Einstellungen geklärt.
- [x] Mew-Startertausch als vorgemerkter Gameplayumfang dokumentiert.
- [ ] Vor Release Zielversion/Updatename und unterstützte Ausgangsversion festlegen.
- [ ] Klären, ob lokaler Quellstand genügt oder Gleichheit zu einer offiziellen Veröffentlichung zwingend ist. Bei Letzterem zuerst passende Quellen/Belege beschaffen.

**Abnahme:** Releaseumfang und Ausgangsversion sind explizit dokumentiert; keine erfundene Releasegleichheit.

### [x] Phase 3 – Hostqualität und Layoutschutz: 100 % des definierten Umfangs

**Womit:** Python 3.11, Pillow, Node 22, GCC/G++, GNU Make, reale C++-Generatorregressionen.

- [x] Fehler im temporären C-Parser-Verfahren behoben, Regressionen vorhanden.
- [x] Strenge JSON-/Referenz-/ID-/Datei-/Fingerprintprüfungen vorhanden.
- [x] **136 Hosttests bestanden**: 20 Prüfer/Mapgenerator, 5 Shader, 71 Dokumentation, 4 Lernset, 4 QR, 32 Node.
- [x] 26 Layoutgrößenunterschiede eingeordnet: **7 bereits ausgeschlossen, 19 ausschließlich Überschussdaten**.
- [x] Keine Kartendaten, Maße oder IDs blind verändert. Kurze/ungerade ausgegebene Puffer werden abgewiesen; IDs gegen vorherigen Generatorstand geprüft.

**Wichtig:** Fehlender direkter Kartenverweis beweist keine Unerreichbarkeit. Birch-Labor enthält gemeinsam eingebundene Skripte und Layoutwechsel. Keine pauschale Quarantäne oder zusätzlichen NULL-Einträge einführen.

**Abnahme:** `python scripts/check.py` grün. Das ist keine vollständige semantische Prüfung des gesamten Spiels.

### [ ] Phase 4 – Shader: 80 %

**Womit:** Manifesttests, fixiertes `@webgpu/glslang` 0.0.15/WASM, später tatsächlicher Slang-/GPU-Host.

- [x] Drei gewünschte Effekte als minimales Preset integriert; Lizenzen erhalten.
- [x] Alle **16 Stufen der acht Preset-Shader zu SPIR-V kompiliert**.
- [x] Drei Regressionstests des Compilerhelfers bestanden.
- [x] Eigener CI-Job erfolgreich, siehe Abschnitt 4.
- [ ] Preset auf unterstütztem GPU-Host tatsächlich laden, Host-Link-/Reflectionprobleme ausschließen.
- [ ] Repräsentative Spielszenen rendern: Text, Bewegung, Innen-/Außenkarte und Kampf. Effektfolge und Bildfehler dokumentieren.

**Abnahme:** Tatsächlicher Rendernachweis und visuelle Freigabe, nicht nur Compilererfolg. Keine Emulator-Einstellungen versionieren.

### [x] Phase 5 – Browserintegration: 100 % des vorhandenen Tests

**Womit:** Playwright, Chromium, HTTP-Server, bestehende Websiteassets.

- [x] Suche, Navigation, Details, Links, Themes, Überlauf und Konsolenfehler geprüft.
- [x] **1280/390/320 Pixel** lokal mit Chromium 153 erfolgreich.
- [x] Veraltete Speed-Label-Erwartung korrigiert; Zahlen weiterhin exakt geprüft.
- [x] Optionaler `CHROMIUM_EXECUTABLE_PATH`; separater CI-Job ebenfalls erfolgreich.

**Grenze:** Kein vollständiger Nachweis für sämtliche Browser oder Barrierefreiheit.

### [ ] Phase 6 – ARM-Build und Zieltests: 25 %

**Womit:** GitHub Actions Ubuntu 24.04, ARM GCC/Binutils/Newlib und bestehende Make-Ziele.

- [x] Separater Job mit protokollierten Compilerversionen eingerichtet und gestartet.
- [ ] Für **aktuellen PR-Commit** Erfolg von `make -j2 all` bestätigen.
- [ ] Anschließend Erfolg von `make -j2 check-all` bestätigen.
- [ ] Bei Fehlern konkrete Logs auswerten, Ursache beheben, kompletten Job erneut prüfen.
- [ ] Erfolgreichen Commit, Lauf-URL und Toolchainversionen im Bericht festhalten.

**Abnahme:** Beide Schritte erfolgreich im selben zu freigebenden Quellstand. Distributionstoolchain ist noch nicht hermetisch fixiert.

### [ ] Phase 7 – Mew-Startertausch: 0 %

**Womit:** Suche in C-/Skript-/Startertabellen, ARM-Build, Regressionstest und Spielprüfung.

- [ ] Tatsächliche Auswahl- und Vergabelogik der neun Starter finden; nicht nur sichtbaren Text ändern.
- [ ] Einen der neun Starter gezielt durch Mew ersetzen. Auswahltext, Vorschau, vergebene Spezies und gegebenenfalls abhängige Zuordnungen prüfen.
- [ ] Test ergänzen, dass die Auswahl wirklich Mew vergibt und die übrigen acht Einträge unverändert bleiben.
- [ ] Im Spiel neues Spiel starten, Mew wählen, Status/Attacken prüfen, speichern und neu laden.

**Abnahme:** Nachweis im Spiel plus grüner Build/Tests. Aktuell noch keine Gameplayänderung enthalten.

### [ ] Phase 8 – Saves: 0 %

**Womit:** Gesicherte, nicht öffentlich versionierte Teststände, dokumentierte Ausgangsversionen, Spiel-Lade-/Schreib-/Reloadtests.

- [ ] Vom Nutzer geeignete Teststände mit genauer Spielversion und Sicherungskopie beschaffen.
- [ ] Unterstützte Ausgangsversionen explizit begrenzen.
- [ ] Repräsentative Stände laden: früh, fortgeschritten, Boxen/Team/Inventar und besondere Spielfortschritte.
- [ ] Änderungen auf Kopien speichern, vollständig neu starten und erneut laden; Inhalte vergleichen.
- [ ] Bei Inkompatibilität Ursache/Migrationsbedarf dokumentieren; nicht still kompatibel nennen.

**Abnahme:** Versionierte Ergebnismatrix ohne private Saveinhalte. Bekannte Strukturgrößen sind kein Kompatibilitätsbeweis.

### [ ] Phase 9 – Spielregressionen: 0 %

**Womit:** Gebaute eigene ROM in geeigneter Laufzeit, strukturierte Testfälle; Einstellungen bleiben außerhalb des Projekts.

- [ ] Start/Neues Spiel/Startervergabe und Laden prüfen.
- [ ] Kartenwechsel, Innen-/Außenräume, NPC-/Storyskripte und relevante Layoutwechsel prüfen.
- [ ] Wild-/Trainerkampf, Fangen, Entwicklung, Items, Team und Boxen prüfen.
- [ ] Für unveränderten Umfang gezielte Smoke-Tests; für geänderte Pfade vertiefte Tests und angemessenen Fortschritts-/Durchspieltest festlegen.
- [ ] Fehler mit Commit, reproduzierbaren Schritten und Erwartung protokollieren; nach Korrektur erneut testen.

**Abnahme:** Vereinbarte Testmatrix vollständig grün, keine offenen Releaseblocker. Hosttests nicht als Spieltest zählen.

### [ ] Phase 10 – Fertiges Spielupdate: 0 %

**Womit:** Releasecheckliste, Git/gh, geeignetes Patchwerkzeug nach Festlegung des Zielformats, Prüfsummen und Lizenzprüfung.

- [ ] Releaseblocker aus Phasen 2, 4, 6–9 schließen oder ausdrücklich mit Nutzer als Einschränkung vereinbaren.
- [ ] Version/Changelog, Buildcommit, Toolchain und unterstützte Ausgangsdatei mit Prüfsumme dokumentieren.
- [ ] Asset-/Lizenz-/Weitergaberechte prüfen. Keine pauschale Rechtefreigabe aus vorhandenem Repository ableiten.
- [ ] Nur zulässiges Patchpaket vorbereiten, keine vollständige ROM/BIOS/private Saves veröffentlichen.
- [ ] Patch auf sauberer erlaubter Ausgangsdatei anwenden und Ergebnis prüfen.
- [ ] Nutzerreview und Merge abwarten; Veröffentlichung erst mit passender Autorisierung.

**Abnahme:** Reproduzierbar anwendbares, getestetes und freigegebenes Update mit bekannten Einschränkungen. Siehe `docs/RELEASE-CHECKLIST.md`.

## 4. Aktueller CI-Snapshot

Direkt am 9. November 2026 über `gh pr view 7 --json statusCheckRollup` geprüft:

Lauf [42617887983](https://github.com/ohZugghkkn-tech/pokemon-romehack/actions/runs/42617887983), PR-Codecommit `dc475952`:

| Job | Tatsächlicher Status beim Abruf |
|---|---|
| `host-tests` | **SUCCESS** |
| `shader-and-browser-tests` | **SUCCESS** |
| `target-build-and-tests` | **IN_PROGRESS**, kein Erfolg bestätigt |

Diese Übergabedokumentation löst nach dem Push einen neuen PR-Lauf aus. **Obiger Snapshot gilt nicht automatisch für den danach neuesten Commit.** Vor Merge erneut prüfen, keine älteren grünen Dependabot-Läufe als ROM-Nachweis verwenden.

## 5. Sofortige To-do-Reihenfolge für die nächste KI

1. **P0:** `git status` und neuesten PR-Commit prüfen; aktuelle CI abfragen. ARM-Job bis zum tatsächlichen Ergebnis verfolgen. Bei Fehlern zuerst dessen Logs bearbeiten.
2. **P1:** Mew-Starterpfad untersuchen und den kleinen genehmigten Gameplaytausch mit Tests umsetzen; damit vorherige Buildnachweise nicht als Nachweis der neuen Änderung ausgeben.
3. **P1:** Ziel-/Save-Ausgangsversion mit Nutzer klären und geeignete Teststände beschaffen. Fehlen sie, diesen Blocker ausdrücklich stehen lassen.
4. **P1:** GPU-Renderprüfung und Spieltestmatrix ausführen, soweit Laufzeit vorhanden; sonst konkrete fehlende Voraussetzung nennen.
5. **P2:** Releasepaket und Versionsdokumentation erst nach den Prüfungen vorbereiten. Nutzer mergen lassen.

Nicht erneut als Arbeit verbuchen: Quellen neu importieren, Submodule einführen, Shader neu erfinden, alle Layoutdateien auf Verdacht kürzen, aus CI-Definitionen Testerfolge ableiten.

## 6. Einstiegskommandos und Dokumente

```bash
# Repository-Root, bestehender Branch
 git status --short
 gh pr view 7 --json headRefOid,state,statusCheckRollup,url
 gh pr checks 7

# Hostprüfungen, vorher venv/Pillow gemäß TESTING.md einrichten
 python scripts/check.py

# Shader inklusive tatsächlicher Kompilierung
 npm ci --prefix scripts/shader-tools --ignore-scripts
 npm test --prefix scripts/shader-tools

# ARM nur in Umgebung mit den dokumentierten Buildabhängigkeiten
 make -C soulgold -j2 all
 make -C soulgold -j2 check-all
```

Browserbefehle und Voraussetzungen: `TESTING.md`. Architektur-/Herkunftskontext: `ROMHACK-WISSEN.md`. Historie: `AUDIT.md`. Letzte lokale Prüfergebnisse und Grenzen: `docs/reviews/2026-11-09-followup.md`. Veröffentlichungsabnahme: `docs/RELEASE-CHECKLIST.md`.

## 7. Aktualisierungsregel für weitere KI-Sitzungen

Nach jeder Arbeitsrunde: Commit/Lauf-URL und tatsächliches Ergebnis ergänzen, erledigte Kästchen nur mit Beleg setzen, Prozente aus obiger Gewichtung neu berechnen und verbleibende Blocker nennen. Änderungen am Umfang zuerst kenntlich machen. Nie 100 % Gesamtfortschritt melden, solange vereinbarte Abnahmen fehlen. Keine feste Fertigstellungszeit aus diesen Prozenten ableiten.
