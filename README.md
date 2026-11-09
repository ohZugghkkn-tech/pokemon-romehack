# pokemon-romehack

Planung und Arbeitsgrundlage für persönliche Erweiterungen von Pokémon SoulGold (Emerald/GBA).

## Inhalt

- [ROMHACK-WISSEN.md](ROMHACK-WISSEN.md): Auf unseren SoulGold-Quellstand spezialisierte Codekarte, Build-/Save-Risiken und Vorlage für den nächsten Änderungsauftrag.
- `soulgold/`: Vollständig übernommene, unveränderte Upstream-Dateien von Release 1.2.1 — kein Submodul.
- [shaders/](shaders/README.md): Fertige ScaleFX-, Bevel- und Image-Adjustment-Shader mit Abhängigkeiten, Lizenzhinweisen und minimalem gemeinsamen Preset. Keine Emulator-Konfiguration.

## Herkunft und Version

- Upstream: https://github.com/Eemeliri/soulgold
- Release: **1.2.1**
- Ursprünglicher Commit: `e73803309e78231142160b3e1029df884bc8b5f1`
- Release-Notizen: https://github.com/Eemeliri/soulgold/releases/tag/1.2.1

Alle in diesem Upstream-Commit versionierten Dateien wurden unter `soulgold/` direkt in dieses Repository übernommen, einschließlich der dortigen Dokumentation und Ignore-Regeln. Die Upstream-Git-Historie ist nicht Teil dieses Verzeichnisses. Ein normaler Klon dieses Repositories reicht aus; Submodul-Befehle sind nicht erforderlich. Eigene spätere Änderungen lassen sich direkt im selben Repository versionieren.

## Aktueller Status

SoulGold wurde eingebunden, aber nicht inhaltlich verändert oder gebaut. Es wurden keine zusätzlichen ROMs oder BIOS-Dateien beschafft; übernommen wurden die versionierten Upstream-Dateien. Es wurden keine Emulatortests ausgeführt. Build-Anleitung, Nutzungsbedingungen und Anforderungen des konkreten Quellstands müssen vor einer Implementierung geprüft werden.

**Wichtige Einschränkung:** Das eingebundene Upstream-README erklärt ausdrücklich, dass dieser Quellstand etwas hinter der veröffentlichten Spielversion liegt. Tag und Versionsanzeige 1.2.1 belegen daher nicht, dass ein Build die veröffentlichte ROM 1.2.1 reproduziert. Die Kompatibilität vorhandener Spielstände ist ungeprüft. Details und belegte Einstiegspunkte stehen in der Wissensdatei.

Als Nächstes wird ein konkreter Änderungsauftrag formuliert; eine Feature-Implementierung ist noch nicht beauftragt.
