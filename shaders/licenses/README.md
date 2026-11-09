# Herkunft und Lizenzhinweise

Upstream: https://github.com/libretro/slang-shaders

Commit: `2345ee91602a7404d3a1a6a5df6108d7305fdad4`

Es gibt keine pauschale einheitliche Lizenzannahme für die gesamte Sammlung. Maßgeblich sind die Hinweise in den einzelnen übernommenen Dateien:

| Dateien unter `upstream/` | Originalhinweis |
|---|---|
| `edge-smoothing/scalefx/shaders/scalefx-pass0.slang` bis `scalefx-pass4.slang` | Copyright (c) 2016 Sp00kyFox; vollständiger MIT-Lizenztext in jedem Shader |
| `handheld/shaders/bevel.slang` | Copyright (C) 2011–2014 Hyllian/Jararaca; GPL Version 2 oder später |
| `misc/shaders/image-adjustment.slang` | Author: hunterk; License: Public domain |
| `include/colorspace-tools.h` | Port aus Asmodean's PsxFX Shader Suite v2.00; NTSC-Code von SimoneT, Jzazbz-Code von torridgristle; GPL v2+ |
| `stock.slang` und die drei Original-`.slangp`-Dateien | Kein eigener Lizenzvermerk in diesen Dateien; unverändert aus dem genannten Commit übernommen. Keine zusätzliche Lizenzbehauptung. |

Der vollständige GPL-v2-Text ist in [`GPL-2.0.txt`](GPL-2.0.txt) beigelegt, übernommen aus der lokalen Systemkopie `/usr/share/common-licenses/GPL-2`. Alle ursprünglichen Quellkommentare bleiben erhalten; es werden keine kompilierten Shader ohne Quellen verteilt.

Das eigene Preset `../soulgold-vivid-relief.slangp` wird unter GPL-2.0-or-later bereitgestellt. Diese Kennzeichnung erklärt nicht pauschal SoulGold, das Hauptrepository oder anders lizenzierte Upstream-Dateien zu GPL-Code. Bei weiterer Distribution sind die jeweiligen Hinweise beizubehalten; die Lizenzlage der Dateien ohne ausdrücklichen Vermerk ist vor einer andersartigen Weiterverwertung gesondert zu klären.
