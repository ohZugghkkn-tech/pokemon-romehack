# Freigabecheckliste — aktuell keine veröffentlichungsreife Version bestätigt

Ein grüner Host-Testjob bedeutet nur: Der benannte Host-Testumfang besteht. Es gibt keinen automatischen Release-Workflow in diesem Hauptrepository.

## Vor einer Veröffentlichung belegen

- [ ] Verwendeten Hauptrepository-Commit, SoulGold-Herkunft, lokale Änderungen und Buildkonfiguration festhalten.
- [ ] Ziel-ROM in dokumentierter Umgebung bauen; Compiler-/Toolversionen, Log und Ergebnis-Hash festhalten.
- [ ] `check-all` vollständig ausführen; Fehler, bekannte Fehler und Skips getrennt zählen.
- [ ] Spiel starten; betroffene Abläufe, Abbruchfälle und Kartenübergänge prüfen.
- [ ] Bei Übernahme bestehender Saves: unterstützte Ausgangsversionen dokumentieren und Laden → Spielen → Speichern → Neustart mit Testkopien prüfen.
- [ ] Alle 26 bekannten Layoutgrößenabweichungen prüfen: korrigierte Quelle oder belegte Nichtverwendung/Ungefährlichkeit, nicht nur „Datei vorhanden“.
- [ ] Shader kompilieren, relative Pfade in einer frischen Kopie prüfen und gemeinsamen Effekt visuell abnehmen.
- [ ] Herkunft und Rechte aller neu verteilten Dateien klären; offene Lizenzzuordnungen nicht als gelöst ausgeben.
- [ ] Falls Patch: exakte Ausgangsdatei mit Prüfsumme, korrektes Ziel und byteidentischen Roundtrip nachweisen. Keine vollständige ROM hochladen.
- [ ] Eigene Versionskennung wählen; nicht den Eindruck einer offiziellen unveränderten SoulGold-Version erwecken.
- [ ] README, bekannte Probleme und Rollback-/Updatehinweise aktualisieren; menschliche Freigabe einholen.

## Derzeitige Blocker

| Bereich | Stand |
|---|---|
| Gleichheit zum offiziellen SoulGold-Release | laut Upstream nicht zugesichert; Zielbasis muss ausdrücklich akzeptiert werden |
| 26 Layoutgrößenabweichungen | exakt inventarisiert, aber inhaltlich nicht geklärt |
| ARM-Build / vollständige Zieltests | CI-Job eingerichtet, Ausführungsergebnis noch ausstehend; lokal Toolchain nicht vorhanden |
| Shaderkompilierung / visueller Vergleich | ausstehend |
| Save-Kompatibilität | ausstehend |
| Browserintegration | ausstehend; kein Freigabekriterium für reine ROM-Änderungen, aber für Websiteänderungen |
| Umfassende Asset-Rechte / einzelne Shader-Hinweise | nicht vollständig geklärt |

Nicht jede offene Aufgabe blockiert einen internen Quellcode-PR. Sie blockiert aber eine entsprechende Behauptung zur Spielbarkeit, Kompatibilität, Optik oder Weiterverteilbarkeit. Ob ein belegter Legacy-Datensatz für ein konkretes Release irrelevant ist, muss der Review dokumentieren.
