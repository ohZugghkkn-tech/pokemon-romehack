# SoulGold Vivid Relief

Fertige Shader, direkt versioniert — kein Submodul und kein Download zur Laufzeit. Übernommen wurde nur die vollständige Abhängigkeitsmenge der drei gewählten Effekte, nicht die gesamte libretro-Sammlung.

## Inhalt

- **ScaleFX** von Sp00kyFox: Kantenglättung für Pixelgrafik, unveränderte Standardkette mit sechs Durchläufen einschließlich Referenzpass.
- **Bevel** von Hyllian/Jararaca: plastischer Pixeleffekt.
- **Image Adjustment** von hunterk: Farbanpassung einschließlich Sättigung.
- [`soulgold-vivid-relief.slangp`](soulgold-vivid-relief.slangp): minimales gemeinsames Preset mit acht Durchläufen.

Herkunft: https://github.com/libretro/slang-shaders

Fixierter Commit: [`2345ee91602a7404d3a1a6a5df6108d7305fdad4`](https://github.com/libretro/slang-shaders/tree/2345ee91602a7404d3a1a6a5df6108d7305fdad4)

Die 12 Dateien unter `upstream/` sind unverändert übernommen. Pfade und SHA-256-Werte stehen in [`upstream-manifest.json`](upstream-manifest.json). Alle drei Originalpresets sind zusätzlich enthalten; gemeinsam genutzte Dateien liegen nur einmal vor. Die externe Arbeitskopie für die Übernahme wurde geklont; im Projekt liegen normale Dateien ohne verschachteltes Git-Repository.

## Minimales Preset

```text
ScaleFX (Referenz + fünf Effektpässe, Ausgabe 3×)
    → Bevel (Ausgabegröße)
    → Image Adjustment (vorherige Größe beibehalten)
```

Zwei Parameter sind explizit gesetzt:

| Parameter | Startwert |
|---|---:|
| `BEVEL_LEVEL` | `0.10` |
| `ia_saturation` | `1.20` |

Andere Effektparameter behalten ihre Upstream-Standardwerte. ScaleFX-Aliase und Float-Zwischenpuffer bleiben erhalten. Der letzte Farbpass behält die Größe des Bevel-Passes bei, statt auf die ursprüngliche GBA-Auflösung zurückzuskalieren.

**Präzisierung:** Bevel berechnet sein Muster anhand von `OriginalSize`, also dem ursprünglichen Pixelraster, und liest die Farbe aus dem vorher geglätteten Bild. Es verwendet nicht einfach das dreifach vergrößerte ScaleFX-Raster für sein Reliefmuster. Auch `BEVEL_LEVEL = 0` ist im Originalcode kein garantierter Aus-Schalter.

Die Werte sind ein Ausgangspunkt, kein visuell abgestimmtes Endergebnis. Keine neuen 4K-Texturen, echte 3D-Geometrie oder garantierte Bildqualität. Es wurde kein Shaderalgorithmus neu geschrieben.

## Verwendung und Umfang

Das gemeinsame Preset in einem Slang-kompatiblen Host, beispielsweise RetroArch, laden. Den Ordner zusammenhalten: Das Preset referenziert `upstream/` mit relativen Pfaden. Die Shader werden außerhalb der GBA-ROM ausgeführt.

**Keine Emulator-Konfiguration enthalten:** keine Treiberauswahl, Auflösung, Vollbild- oder Seitenverhältniseinstellung. Die Größenangaben im Preset sind notwendige interne Shader-Pass-Skalierung, keine Einstellung der Bildschirmauflösung.

## Lizenzen

Siehe [`licenses/README.md`](licenses/README.md). Originale Autoren- und Lizenzhinweise sind in den Quellen erhalten. GPL-v2-Text liegt bei. Insbesondere ist der von Image Adjustment eingebundene Header GPL-2.0-or-later, obwohl die Hauptdatei als Public Domain gekennzeichnet ist.

## Prüfungen

Vom Repository-Root:

```bash
python3 -m unittest discover -s shaders/tests -v
```

Die Tests prüfen Manifest-Hashes, lokale Preset- und Include-Abhängigkeiten, Pass-Reihenfolge, ScaleFX-Einstellungen sowie Parameternamen und Wertebereiche. Sie ersetzen weder die Shaderkompilierung im Host noch einen visuellen Test.

**Status:** statische Prüfungen ausgeführt; kein RetroArch-/GPU-Test, keine visuelle Abnahme. SoulGold-Code und Starterauswahl sind unverändert.

### Tatsächliche Offline-Kompilierung

Zusätzlich: `npm ci --prefix scripts/shader-tools --ignore-scripts` und `npm test --prefix scripts/shader-tools` vom Repository-Root. Am 9. November 2026 erfolgreich: acht Preset-Shader / 16 Stufen nach SPIR-V. Das ersetzt weiterhin keinen GPU-/RetroArch-Bildtest. Siehe `TESTING.md`.
