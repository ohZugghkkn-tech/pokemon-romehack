# Zweite, skeptische Prüfung: Repositorydesign und Aussagekraft

Datum: 9. November 2026. Dies ist ein **Gegenreview zur ersten Prüfung**, nicht deren bloße Bestätigung. Alle Vergleichsquellen wurden öffentlich über GitHub gelesen; kein fremder Code wurde für die Designregeln übernommen.

## 1. Maßstab: etablierte Projekte, nicht Popularität als Qualitätsbeweis

Die Sterne sind eine Momentaufnahme der GitHub-API, keine Downloads, Sicherheitsbewertung oder Garantie für Fehlerfreiheit. Ein fortlaufend entwickeltes Projekt wird hier nicht als „vollständig fertig und fehlerfrei“ bezeichnet.

| Referenz | Abgelesener Stand | Konkreter beobachteter Maßstab |
|---|---|---|
| [pret/pokeemerald](https://github.com/pret/pokeemerald/tree/731ad5bfd6e6f265508d0efcca0ba42f9dcf5881) | 3.672 Sterne | [CI](https://github.com/pret/pokeemerald/blob/731ad5bfd6e6f265508d0efcca0ba42f9dcf5881/.github/workflows/build.yml) unterscheidet Matching-/Compare-Build und Modern-Build; Host-Syntax allein genügt nicht |
| [rh-hideout/pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion/tree/8b10030b4c42f2b481567bcf43eb46eb64679d93) | 920 Sterne | [CI](https://github.com/rh-hideout/pokeemerald-expansion/blob/8b10030b4c42f2b481567bcf43eb46eb64679d93/.github/workflows/build.yml) trennt ROM-, Release- und Zieltestjobs; explizites Build-Gate |
| [Modern Emerald](https://github.com/resetes12/pokeemerald/tree/e983cc52f7d9cde0a54ff2fc430f653c26086c8c) | 210 Sterne; [veröffentlichtes Release 3.6](https://github.com/resetes12/pokeemerald/releases/tag/Release3.6) | [README](https://github.com/resetes12/pokeemerald/blob/e983cc52f7d9cde0a54ff2fc430f653c26086c8c/README.md) trennt Spiel, Varianten und verwandte Projekte und nennt versionsbezogene Save-Grenzen; kein allgemeines Kompatibilitätsversprechen |
| [mGBA](https://github.com/mgba-emu/mgba/tree/662dada8b79070bde93829a44d583c517fc5ec2d) | 7.580 Sterne | [Beitragsregeln](https://github.com/mgba-emu/mgba/blob/662dada8b79070bde93829a44d583c517fc5ec2d/CONTRIBUTING.md) verlangen genaue Build-/Systemangaben, reproduzierbare Fehler und Komponentenbezug |
| [libretro/slang-shaders](https://github.com/libretro/slang-shaders/tree/2345ee91602a7404d3a1a6a5df6108d7305fdad4) | 478 Sterne | [Slang-Spezifikation](https://github.com/libretro/slang-shaders/blob/2345ee91602a7404d3a1a6a5df6108d7305fdad4/README.md) beschreibt Passketten und Auflösungen; vorhandene Dateien allein belegen kein korrekt gerendertes Bild |

**Nicht blind kopiert:** pret-Matching mit Original-ROM-Hash passt nicht zum modifizierten SoulGold. Expansion-Builds für FireRed/LeafGreen erweitern unseren Scope nicht. mGBA hat eigene Stil-, Lizenz- und ausdrücklich Anti-KI-Beitragsregeln; wir reichen dort keinen KI-Code ein und übernehmen diese Regeln nicht als vermeintliche Lizenz unseres Projekts. Fremde Release-/Schreibworkflows werden nicht aktiviert.

## 2. Kritik an der ersten Prüfung

### P1 — Zu schwacher Hauptnachweis

116 Hosttests waren ein nützlicher Befund, aber kein Maß für den Zustand der Spiel-ROM. Der zentrale Teil des Repositories ist C/Assembler für ARM. Der erste CI-Entwurf hätte dauerhaft grün sein können, ohne diesen Teil jemals zu bauen.

**Korrektur:** eigener Job `target-build-and-tests` für normalen ARM-Build und `check-all`, mit Arbeitsverzeichnis `soulgold/`, begrenzter Parallelität und ohne ROM-Upload. **Noch kein bestandenes GitHub-Ergebnis.** Host- und Zielprüfungen bleiben im Namen und Bericht getrennt. Keine Behauptung eines hermetischen Builds: Ubuntu-Pakete sind weiterhin distributionsabhängig; Compiler werden im Job protokolliert.

### P1 — „Layoutdateien vorhanden“ verwechselte Existenz mit Integrität

Eine Blockkarte enthält 16-Bit-Metatiles; das unveränderte `tools/mapjson/mapjson.cpp` bindet Blockdaten ein und schreibt Breite/Höhe separat. Der erste Scanner prüfte nur, ob die Datei existiert. Ein Längenfehler blieb unsichtbar.

**Neuer Befund:** 26 Layouts haben eine andere Länge als `width × height × 2`. Konkrete Beispiele:

- `LAYOUT_MART`: 11×9 erwartet 198 Bytes, vorhanden 176.
- `LAYOUT_PETALBURG_WOODS`: 54×44 erwartet 4.752, vorhanden 4.224.
- `LAYOUT_UNUSED_CAVE1`: 9×10 erwartet 180, vorhanden 4.

Einige andere Datensätze besitzen nur zusätzliche Bytes. „Abweichung“ ist deshalb noch kein Beweis für einen tatsächlich ausgelösten Laufzeitfehler. `map_groups.json` registriert auch Legacy-Karten; die Registrierung beweist keine Erreichbarkeit im Johto-Spiel.

**Korrektur der Prüfung, nicht der unbekannten Spielabsicht:** Datenpfade, Dimensionen, tatsächliche/erwartete Größe und Hash werden in `docs/known-layout-issues.json` explizit festgehalten. Neue/geänderte Abweichungen und veraltete Debt-Einträge lassen den Scanner scheitern. Die bekannte Schuld wird deutlich ausgegeben und bleibt offen. **Diese Liste macht die 26 Datenfehler nicht richtig.** Ihre Spielwirkung muss durch Erreichbarkeitsanalyse und Zieltests geklärt werden; Auffüllen/Abschneiden wäre ohne diese Belege verantwortungslos.

### P2 — Prüfer hatte selbst keine Tests und übersah neue Dateien

Der erste Syntaxscanner verwendete nur `git ls-files`. Damit prüfte er ausgerechnet die neu geschriebenen, noch unversionierten Prüfskripte nicht. Außerdem fehlten Tests für dessen eigene Fehlermeldungen.

**Korrektur:** versionierte und nicht ignorierte neue Dateien einbeziehen, Pfadgrenzen prüfen, doppelte Gruppen/Karten-/Layout-IDs und unbekannte Layoutverweise erkennen. 14 neue Regressionstests testen richtige und falsche Fälle, einschließlich doppelter JSON-Schlüssel, neuer/veränderter/staler Debt und doppelter Map-IDs.

### P2 — Herkunft, lokale Änderungen und Veröffentlichung waren nicht sauber getrennt

Ein großes Quellverzeichnis mit unveränderter Upstream-Versionsanzeige kann fälschlich als offizielles reproduzierbares Release verstanden werden. Unser Source-Tag enthält bereits den gegenteiligen Upstream-Hinweis.

**Designkorrektur:** `UPSTREAM.json` als Herkunftsindex; `docs/upstream-changes.md` dokumentiert die lokalen Eingriffe. Keine neue offizielle Versionsbehauptung und kein automatischer Upstream-Pull. Shader und Spiel bleiben getrennte Komponenten. Kein Root-Lizenztext, der fremde Assets pauschal neu lizenziert.

### P2 — Root-Arbeitsablauf und Reviewkontrakt fehlten

Ein riesiges Vendor-Verzeichnis braucht nicht mehr abstrakte Agentenrollen, sondern wenige klare Einstiegspunkte und Regeln.

**Designkorrektur:** Root-`Makefile` mit `help`, `check`, `rom`, `target-tests`; `CONTRIBUTING.md`; Root-PR-Vorlage; explizite Release-Checkliste mit offenen Blockern. Keine Umstrukturierung von 47.000 Dateien nur für eine schönere Ordnergrafik. Die vollständige Einbindung bleibt erhalten, wie vom Nutzer gewünscht.

### P2 — CI-Abhängigkeiten waren beweglich

Die Action-Referenzen `@v4`/`@v5` können sich ändern.

**Korrektur:** in GitHub geprüfte volle Commit-IDs der verwendeten Actions, nur lesende Rechte, keine persistierten Checkout-Credentials, Zeitlimits und Abbruch überholter Läufe. Dependabot kann diese Pins und die Root-Python-Abhängigkeit per PR aktualisieren; kein Auto-Merge. Das ist Risikoreduktion, keine vollständige Supply-Chain-Sicherung.

### P3 — Der angeglichene Item-Test war kein Gameplayfix

„after showing Shaymin“ und „by showing Shaymin“ unterschieden sich nur in der Darstellung. Den Test an den bestehenden Text anzupassen war keine Reparatur einer Spielmechanik. Die ursprüngliche Erklärung war im Audit korrekt eingegrenzt, darf aber nicht als großer Bugfix verkauft werden. Ein unabhängiger Scriptbefund bestätigt den Shaymin-/Gracidea-Zweig, nicht die Wahl eines englischen Wortes.

## 3. Bewusste Nicht-Änderungen

- Keine 26 Binärkarten auf Verdacht geändert.
- Keine Save-Struktur, IDs oder Starter verändert.
- Keine ganze Engine aktualisiert, um vermeintlich automatisch alle Bugs zu beheben.
- Keine Dateien aus unklaren Lizenzgründen still gelöscht; keine Rechte erfunden.
- Keine Emulator-Einstellungen hinzugefügt.
- Kein einzelner „alles bestanden“-Status für ROM, Shader, Browser und Host zusammen behauptet.

## 4. Aktuelles Urteil

Das Repository ist nach diesen Änderungen **besser überprüfbar und klarer abgegrenzt**, aber **nicht als fertiges getestetes Spielrelease freigegeben**. Ausgeführte Hosttests, CI-Definitionen und offene Freigabeanforderungen sind getrennte Belege.

Die nächste wertvolle technische Arbeit ist nicht noch mehr Planungsprosa, sondern das Ergebnis des ARM-CI-Jobs, anschließend die gezielte Prüfung der Layoutabweichungen, Save-Tests und ein echter Shadervergleich. Bis dahin bleiben diese Punkte offen.
