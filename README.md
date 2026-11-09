# pokemon-romehack

Planung und Arbeitsgrundlage für persönliche Erweiterungen von Pokémon SoulGold (Emerald/GBA).

## Inhalt

- [ROMHACK-WISSEN.md](ROMHACK-WISSEN.md): Technische Grundlagen und Planungs-/Übergabehinweise für spätere Arbeitssessions.
- `soulgold/`: Vollständig übernommene, unveränderte Upstream-Dateien von Release 1.2.1 — kein Submodul.

## Herkunft und Version

- Upstream: https://github.com/Eemeliri/soulgold
- Release: **1.2.1**
- Ursprünglicher Commit: `e73803309e78231142160b3e1029df884bc8b5f1`
- Release-Notizen: https://github.com/Eemeliri/soulgold/releases/tag/1.2.1

Alle in diesem Upstream-Commit versionierten Dateien wurden unter `soulgold/` direkt in dieses Repository übernommen, einschließlich der dortigen Dokumentation und Ignore-Regeln. Die Upstream-Git-Historie ist nicht Teil dieses Verzeichnisses. Ein normaler Klon dieses Repositories reicht aus; Submodul-Befehle sind nicht erforderlich. Eigene spätere Änderungen lassen sich direkt im selben Repository versionieren.

## Aktueller Status

SoulGold wurde eingebunden, aber nicht inhaltlich verändert oder gebaut. Es wurden keine zusätzlichen ROMs oder BIOS-Dateien beschafft; übernommen wurden die versionierten Upstream-Dateien. Es wurden keine Emulatortests ausgeführt. Build-Anleitung, Nutzungsbedingungen und Anforderungen des konkreten Quellstands müssen vor einer Implementierung geprüft werden.

Die früheren Aussagen „kein Zielprojekt heruntergeladen“ in der Wissensdatei dokumentieren den damaligen Planungsstand. Mit der jetzigen Freigabe wurde der Quellcode eingebunden; eine Feature-Implementierung ist noch nicht beauftragt.
