# pokemon-romehack

Planung und Arbeitsgrundlage für persönliche Erweiterungen von Pokémon SoulGold (Emerald/GBA).

## Inhalt

- [ROMHACK-WISSEN.md](ROMHACK-WISSEN.md): Technische Grundlagen und Planungs-/Übergabehinweise für spätere Arbeitssessions.
- `soulgold/`: Unveränderter Upstream-Quellcode als Git-Submodul.

## SoulGold-Version

- Upstream: https://github.com/Eemeliri/soulgold
- Release: **1.2.1**
- Fixierter Commit: `e73803309e78231142160b3e1029df884bc8b5f1`
- Release-Notizen: https://github.com/Eemeliri/soulgold/releases/tag/1.2.1

Das Submodul speichert eine feste Commit-Referenz statt einer zusätzlichen Kopie aller Upstream-Dateien im übergeordneten Git-Verlauf. Der Quellcode ist lokal unter `soulgold/` ausgecheckt. Ein späterer neuer Klon benötigt die Initialisierung:

```bash
git clone --recurse-submodules <URL-dieses-Repositories>
```

Bei einem bereits vorhandenen Klon:

```bash
git submodule update --init --recursive
```

Nicht ungeprüft `git submodule update --remote` verwenden: Damit könnte ein anderer Stand als die hier fixierte Release-Version ausgewählt werden.

## Aktueller Status

SoulGold wurde eingebunden, aber nicht verändert oder gebaut. Es wurden keine ROMs oder BIOS-Dateien hinzugefügt und keine Emulatortests ausgeführt. Die Build-Anleitung, Nutzungsbedingungen und Anforderungen des konkreten Quellstands müssen vor einer Implementierung geprüft werden.

Die früheren Aussagen „kein Zielprojekt heruntergeladen“ in der Wissensdatei dokumentieren den damaligen Planungsstand. Mit der jetzigen Freigabe wurde ausschließlich der Quellcode eingebunden; eine Feature-Implementierung ist noch nicht beauftragt.

Änderungen innerhalb eines Submoduls werden nicht durch einen Commit im Hauptrepository allein gespeichert. Vor einer späteren eigenen SoulGold-Implementierung muss deshalb entschieden werden, wie eigene Änderungen dauerhaft verwaltet werden (beispielsweise freigegebener Fork oder versionierte Patches). Der aktuelle unveränderte Upstream-Stand benötigt keinen eigenen Fork.
