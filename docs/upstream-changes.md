# Eigene Änderungen gegenüber SoulGolds Herkunftsstand

Herkunft: `UPSTREAM.json`. Die vollständige Dateiübernahme ist eine **bewusste Nutzerentscheidung**; sie wird nicht zurück in ein Submodul umgewandelt. Das ist kein neuer Fork mit eigener Enginearchitektur, sondern eine vendorte Spielbasis mit klar abgegrenzten Ergänzungen.

## Lokale Eingriffe in `soulgold/`

| Pfad | Änderung / Grund |
|---|---|
| `INSTALL.md` | Fehlendes Anführungszeichen im Toolchain-Beispiel korrigiert |
| `tools/soulgold_docs/c_parser.py` | Präprozessor liest stdin statt gemeinsamem temporärem Dateipfad |
| `tools/soulgold_docs/tests/test_c_parser.py` | Neue Regressionstests für Parallelität, Aufruf und Fehlerweitergabe |
| `tools/soulgold_docs/tests/test_items.py` | Bestehende Text-Erwartung an den unveränderten Parsertext angeglichen; kein Gameplayfix |

Shader, Root-CI, Host-Runner und Projektdokumentation sind getrennte eigene Komponenten außerhalb von `soulgold/`. Generierte Header und Host-Binaries werden nicht versioniert.

## Updateverfahren

1. Gewünschten **SoulGold**-Commit und dessen Release-Zuordnung prüfen; kein pauschales Engine-Update.
2. Upstream-Diff zum Herkunftscommit getrennt von unseren lokalen Änderungen untersuchen.
3. Save-Layout, gespeicherte IDs, neue Assets/Lizenzhinweise und bekannte Datenabweichungen prüfen.
4. Kleine überprüfbare Änderung vorschlagen, eigene Eingriffe erhalten und Regressionstests ausführen.
5. Erst nach bestätigter Übernahme Herkunftsreferenz, Änderungsliste und gegebenenfalls bekannte Probleme aktualisieren.

**Nicht verwenden:** `git pull RHH ...` im Hauptrepository nach einer geerbten Upstream-Anleitung. Unsere Verzeichnisstruktur und Git-Historie sind anders. Upstream-eigene Workflows und Beitragsregeln sind keine automatische Konfiguration unseres Projekts.

Das ursprüngliche Tree-Hash in `UPSTREAM.json` beschreibt den Import, nicht den heute modifizierten Arbeitsbaum. Der Hash ist ein Herkunftsbeleg, keine aktuelle Aussage „alles unverändert“ und keine vollständige Lizenzfreigabe.
