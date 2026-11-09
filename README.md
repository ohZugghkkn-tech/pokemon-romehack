# SoulGold — persönliche Projektbasis

Vollständig eingebundener **Pokémon-SoulGold-Quellcode** auf Emerald-/GBA-Basis plus separates Shaderpaket. Kein Submodul, kein eigener Emulator und kein nachgewiesen fertiges Spielrelease.

## Komponenten

| Pfad | Aufgabe |
|---|---|
| [`soulgold/`](soulgold/) | Übernommener Spielquellcode mit wenigen dokumentierten lokalen Werkzeugkorrekturen |
| [`shaders/`](shaders/README.md) | ScaleFX → Bevel → Image Adjustment; minimale gemeinsame Effektkette, keine Emulator-Konfiguration |
| [`scripts/`](scripts/) | Host-Prüfungen und eigene Regressionstests |
| [`UPSTREAM.json`](UPSTREAM.json) | Herkunftsstände; lokale Eingriffe in [`docs/upstream-changes.md`](docs/upstream-changes.md) |

Ein normaler Git-Klon enthält alle Projektdateien. Es ist kein Submodul-Update erforderlich. Shader bearbeiten das Bild außerhalb der ROM. Mew als Ersatz für einen Starter ist vorgemerkt, **noch nicht umgesetzt**.

## Einstieg

Voraussetzungen und Einrichtung: **[TESTING.md](TESTING.md)**. Danach vom Repository-Root:

```bash
make help          # Einstiegspunkte anzeigen
make check         # Hostprüfungen; kein Beleg für einen funktionierenden ROM-Build
make rom           # Separater ARM-Build, benötigt Zieltoolchain
make target-tests  # Vollständige ARM-/mGBA-Zieltests
```

Mit eigener Python-Umgebung kann `make PYTHON=.venv/bin/python check` verwendet werden. Es gibt keinen automatischen Download von Spiel-ROMs und keine automatische Veröffentlichung.

## Herkunft und wichtige Grenzen

- SoulGold-Upstream: https://github.com/Eemeliri/soulgold
- Übernommener Tag: **1.2.1**, Commit `e73803309e78231142160b3e1029df884bc8b5f1`.
- Das Upstream-README sagt ausdrücklich, dass dieser Quellstand hinter der veröffentlichten Spielversion liegt. Die Anzeige `v1.2.1` beweist weder dieselben Features noch dieselbe ROM oder Save-Kompatibilität.
- Die Shader stammen unverändert aus einem fixierten libretro-Commit. Die Hauptsammlung hat keine pauschal angenommene einheitliche Lizenz; siehe [Shader-Lizenzhinweise](shaders/licenses/README.md).
- Eine umfassende Rechteprüfung der übernommenen Spielassets ist nicht abgeschlossen. Es wird keine pauschale Root-Lizenz über fremde Werke behauptet.

## Prüfstatus — getrennt nach Beleg

| Bereich | Stand |
|---|---|
| Host-Regressionstests | Lokal erfolgreich; Verfahren in `TESTING.md` |
| Karten-/Layoutprüfung | Referenzen geprüft; **26 bekannte Größenabweichungen offen**, nicht automatisch repariert |
| ARM-Build und Zieltests | CI: ROM-Build auf `main` erfolgreich, `make check-all` fehlgeschlagen (4 Assertions); Ursache dokumentiert, Behebung auf `arena/74dc1344-pokemon-romehack`, grüner Folgelauf ausstehend; lokal keine ARM-Toolchain |
| Shaderkompilierung / visuelle Abnahme | Ausstehend |
| Save-Kompatibilität | Ungeprüft |
| Browserintegration | Separater Test, noch nicht ausgeführt |

**Hosttests sind keine Release-Freigabe.** Bekannte Datenabweichungen: [`docs/known-layout-issues.json`](docs/known-layout-issues.json). Gründe und Grenzen der Korrekturen: [skeptischer Designreview](docs/reviews/2026-11-09-design-review.md).

## Weiterarbeiten

- [CONTRIBUTING.md](CONTRIBUTING.md): kleine nachvollziehbare Änderungen, Zuständigkeiten und Reviewregeln.
- [ROMHACK-WISSEN.md](ROMHACK-WISSEN.md): konkrete Codekarte und Vorlage für den gewünschten Spieleingriff.
- [AUDIT.md](AUDIT.md): erste Prüfung mit ausdrücklich ergänzter Gegenprüfung.
- [Freigabecheckliste](docs/RELEASE-CHECKLIST.md): Anforderungen vor einer Spiel-/Patchveröffentlichung.

Keine Secrets, BIOS-Dateien, vollständigen Spiel-ROMs oder privaten Spielstände hochladen. Bei späteren Änderungen den Ursprung und die lokalen Eingriffe nachvollziehbar halten.
