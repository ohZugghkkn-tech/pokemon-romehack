# SoulGold: technische Projektgrundlage und Übergabeplanung

Stand: 9. November 2026. Diese Datei ist auf den **lokal eingebundenen SoulGold-Quellstand** spezialisiert. Sie ersetzt die bisherige allgemeine ROM-Hacking-Einführung. Ziel ist eine belegte Grundlage, auf der wir anschließend deinen konkreten Änderungsauftrag formulieren können.

**Aktueller Auftrag:** Repository auf Probleme prüfen und belegte Fehler korrigieren. Zusätzlich zur bisherigen Shaderübernahme wurden Host-Testinfrastruktur und Dokumentationswerkzeuge korrigiert. Ergebnisse stehen in [AUDIT.md](AUDIT.md), ausführbare Prüfungen in [TESTING.md](TESTING.md). Keine Gameplayänderung, kein Engine-Update und keine ROM-Veröffentlichung. Der Startertausch zu Mew ist vorgemerkt, aber noch nicht umgesetzt.

## Aktuelle KI-zu-KI-Roadmap

Die [To-do-Liste mit Phasen, Werkzeugen, Abnahmekriterien und gewichtetem Fortschritt](docs/KI-ZU-KI-TODO.md) beschreibt den Weg vom Import bis zum eigenen fertigen Spielupdate. Aktuelle Planung: **rund 55 %**, ausdrücklich keine Qualitäts- oder Spielbarkeitsmessung.

## 1. Welches Projekt wir tatsächlich bearbeiten

| Eigenschaft | Feststellung / Beleg |
|---|---|
| Spiel | Pokémon SoulGold, Johto-Hack auf Emerald-/GBA-Basis, nicht HeartGold/SoulSilver für DS |
| Upstream | https://github.com/Eemeliri/soulgold |
| Übernommener Tag | `1.2.1` |
| Herkunftscommit | `e73803309e78231142160b3e1029df884bc8b5f1` |
| Lokaler Ort | [`soulgold/`](soulgold/) |
| Einbindung | Vollständig versionierte Dateien im Hauptrepository, kein Submodul |
| Versionsanzeige im Code | `DISPLAY_VERSION "v1.2.1"` in [`include/config/version.h`](soulgold/include/config/version.h) |
| Genannte Enginebasis | pokeemerald-expansion 1.15.0 laut [`README.md`](soulgold/README.md) |
| Fachliche Herkunft | Heart & Soul, dessen Expansion-Port und weitere Erweiterungen; siehe Upstream-Credits |

### 1.1 Wichtige Einschränkung: Tag ist nicht gleich veröffentlichte Spiel-ROM

Das lokale Upstream-README beginnt mit dem Hinweis, dass das Repository etwas hinter der veröffentlichten Version liegt. Der Autor habe auf einem Entwicklungsbranch an 2.0 weitergearbeitet und daraus 1.2.0 und 1.2.1 veröffentlicht.

Daraus folgt:

- Wir haben **den Quellstand unter Tag 1.2.1**, nicht den Nachweis einer vollständigen Reproduktion des veröffentlichten Spiels 1.2.1.
- Eine Versionszeichenfolge belegt keine Binärgleichheit.
- Aussagen aus Release-Notizen gelten nicht automatisch für jede Funktion dieses Quellstands.
- Das spätere eigene Ziel kann entweder dieser lokale Stand sein oder ein nachweislich zur veröffentlichten ROM passender Stand. Diese Entscheidung ist noch offen.
- Falls dein vorhandener Spielstand aus der veröffentlichten ROM stammt, ist seine Kompatibilität mit einem Build dieses Repositorys **ungeprüft**.

**Korrektur zur bisherigen Unterhaltung:** Die frühere Formulierung „Release 1.2.1 vollständig übernommen“ bezeichnet die vollständige Dateiübernahme des Tags. Sie darf nicht als Zusicherung verstanden werden, dass sämtliche Features der veröffentlichten ROM enthalten sind.

## 2. Verbindlicher Arbeitsstand

Bereits erledigt:

- SoulGold-Dateien direkt unter `soulgold/` eingebunden.
- Herkunft und Quellstand im Projekt-README dokumentiert.
- Bei der Übernahme wurde der Git-Tree auf identische Dateiinhalte und Dateimodi zum Herkunftscommit geprüft.
- Für diese Spezialisierung lokale Header, Makefile, Konfiguration, Datenquellen und Dokumentation gelesen.
- Im anschließenden Audit und Gegenreview 130 Host-Einzeltests sowie Syntax-, Karten-/Layout- und Musikprüfungen erfolgreich ausgeführt. Dokumentationsparser, Testvorbereitung und Root-CI korrigiert; Einzelheiten in `AUDIT.md`. Das sind keine ROM-/GPU-Testergebnisse. Der Gegenreview fand außerdem 26 bislang ungeklärte Layoutgrößenabweichungen; siehe `docs/known-layout-issues.json` und `docs/reviews/2026-11-09-design-review.md`.

Nicht erledigt:

- Kein SoulGold-Build und kein Emulatortest.
- Keine neue Prüfung der gesamten Übernahme gegen einen Remote-Stand in dieser Dokumentationssession.
- Kein Nachweis der Reproduzierbarkeit der veröffentlichten Spiel-ROM.
- Keine Save-Migration getestet.
- Kein konkretes persönliches Feature ausgewählt oder umgesetzt.
- Keine umfassende Lizenz- und Asset-Rechteprüfung.

**Belegstatus:** „Im Quellcode vorhanden“ ist statisch belegt. „Funktioniert im Spiel“ erfordert einen ausgeführten Test. „Geplant“ bedeutet ausdrücklich nicht „bestanden“.

## 3. So ist unser SoulGold-Code zu bearbeiten

Wir arbeiten mit vorhandenem C-/Assembler-Quellcode und dessen Asset-Pipeline. Binary-Hacking-Werkzeuge, ROM-Repointing und beliebige C-Injection sind **nicht unser Standardweg**.

```text
Änderungswunsch
   → vorhandene SoulGold-Funktion und Datenquellen belegen
   → minimalen Eingriff planen und freigeben
   → Quellcode / Eingabedaten ändern
   → Zielbuild und passende Tests ausführen
   → eigene Version dokumentieren und gegebenenfalls Patch erstellen
```

Es wird kein neues Emerald-Projekt daneben geklont. Anleitungen, die `git clone ...pokeemerald-expansion` empfehlen, beschreiben die allgemeine Upstream-Installation; unsere Arbeitsbasis liegt bereits unter `soulgold/`.

Die alte allgemeine Übersicht zu GB-Banking, Nintendo-DS-NARCs, FireRed/CFRU, IPS-Interna und Binärhooks ist für diesen Auftrag nicht maßgeblich und wurde aus dem aktiven Plan entfernt. Sie ist weiterhin in der Git-Historie des Dokuments nachvollziehbar.

## 4. Codekarte: konkrete Einstiegspunkte

Alle folgenden Pfade beziehen sich auf das vorhandene Verzeichnis `soulgold/`. Sie sind **Einstiegspunkte**, keine bereits freigegebene Änderungsliste. Für einen Auftrag müssen Definitionen, Aufrufer und Tests gemeinsam gelesen werden.

| Bereich | Einstiegspunkte | Vor einer Änderung prüfen |
|---|---|---|
| Build und Ausgabe | `Makefile`, `config.mk`, `INSTALL.md`, `docs/install/` | Toolchain, Flags, generierte Dateien, Speicherverbrauch |
| Hauptschleife / Tasks | `src/main.c`, `src/task.c` | aktiver Callback, Ablauf pro Frame, Aufräumen |
| Spezieswerte | `src/data/pokemon/species_info.h`, `src/data/pokemon/species_info/` | `gSpeciesInfo`, tatsächliche Speziesdefinition, Konfiguration und Formen |
| Attacken | `src/data/moves_info.h`, `include/constants/moves.h` | Datenwirkung gegenüber separater Effektimplementierung |
| Items | `src/data/items.h`, `include/constants/items.h` | Effekte, Preise, Shops und gespeicherte IDs |
| Lernsets | `src/data/pokemon/level_up_learnsets/`, `egg_moves.h`, `all_learnables.json`, `legacy_level_up_config.json` | welche Quelle den betroffenen Eintrag erzeugt; keine generierte Datei blind ändern |
| Trainerteams | `src/data/trainers.party`, `src/data/battle_partners.party`, `trainer_rules.mk` | Eingabedatei statt generiertem Header; betroffene Varianten und Rematches |
| Wilde Begegnungen | `src/data/wild_encounters.json` | Kartenbezug, Tageszeiten und Spezialbegegnungen |
| Karten / NPCs | `data/maps/`, `data/layouts/`, `data/event_scripts.s` | Ereignisbindung, Layout, Scriptquelle, Flags |
| Scriptsystem | `src/script.c`, `data/script_cmd_table.inc`, `data/specials.inc` | `ScriptContext_RunScript`, Befehlshandler, C-Special und gespeicherter Zustand |
| Kampflogik | `src/battle_main.c`, `src/battle_util.c`, `src/battle_util2.c`, `data/battle_scripts_1.s`, `data/battle_scripts_2.s` | Ausführungspfad, Daten, Anzeige und Seiteneffekte |
| Spieloptionen | `src/option_menu.c`, `src/replay_options.c`, `test/gameplay_options.c` | Laufzeitoption gegenüber Compile-Time-Konfiguration und Save-Feld |
| Levelskalierung | `src/level_scaling.c`, `include/config/level_scaling.h`, `src/data/level_scaling_rules.h` | bestehende Regeln und Sonderfälle vor neuer Skalierungslogik |
| Erfolge | `src/achievements.c`, `src/achievements_menu.c`, `src/achievements_popup.c` | Auslöser, Zählung, Belohnungen und Persistenz |
| Hidden Grottos | `src/hidden_grotto.c`, `test/hidden_grotto.c` | Tageswechsel, Generierung und gespeicherte Inhalte |
| Titelverteidigung | `src/title_defense.c`, `test/title_defense.c` | Trainerwahl, Freischaltung und Kampfablauf |
| Speichern | `src/save.c`, `include/save.h`, `include/global.h`, `include/config/save.h` | existierende Layout-Assertions und Konvertierungswege |
| Pokémon-Zugriff | `include/pokemon.h`, `src/pokemon.c` | bestehende Accessor-APIs und kompaktes Datenlayout |
| Eigene Spieldokumentation | `tools/soulgold_docs/`, `docs/src/`, `docs/` | Eingabequelle vs. generierte Ausgabe; Versionswerbung |

### 4.1 Konfiguration ist nicht dasselbe wie Spieloption

In `include/config/` existieren unter anderem `battle.h`, `pokemon.h`, `species_enabled.h`, `overworld.h`, `item.h`, `caps.h`, `dexnav.h`, `follower_npc.h`, `save.h` und `version.h`.

Eine Änderung an einem Build-Schalter kann viele Codepfade betreffen. Vorher prüfen, ob der gewünschte Effekt schon als Spieloption vorliegt und wie der gespeicherte Optionswert verwendet wird. Weder ein neuer Schalter noch ein neues Save-Feld wird ohne konkreten Bedarf angelegt.

### 4.2 Generierte Dateien und doppelte Scriptformate

`trainer_rules.mk` führt `.party`-Dateien durch `trainerproc` und erzeugt beispielsweise `src/data/trainers.h`, `src/data/battle_partners.h` und Testheader. Diese Ausgaben sind nicht die primären Bearbeitungsquellen.

Unter `data/maps/AzaleaTown/` liegen beispielsweise sowohl `scripts.pory` als auch `scripts.inc`. Vor einer Scriptänderung muss die konkrete Generierungsregel und Einbindung geprüft werden. Das bloße Vorhandensein zweier Dateien belegt nicht, dass beide unabhängig zu pflegen sind. `.bak`-Dateien sind kein Nachweis des aktiven Inhalts.

Vor jeder Änderung beantworten: **Welche Datei ist Eingabe, welche Ausgabe und wodurch wird sie neu erzeugt?**

## 5. Tatsächlicher Build dieses Quellstands

Belege: [`Makefile`](soulgold/Makefile), [`config.mk`](soulgold/config.mk), [`INSTALL.md`](soulgold/INSTALL.md), [`Debian-Anleitung`](soulgold/docs/install/linux/DEBIAN.md).

| Einstellung | Im Makefile / in der Konfiguration vorhanden |
|---|---|
| Standard-Spiel | `GAME_VERSION ?= EMERALD`, `GAME_CODE ?= BPEE` |
| Dateiname | `FILE_NAME := Soulgold`, daraus `Soulgold.gba`, `.elf`, `.map` |
| Compiler | ARM-GCC-Werkzeuge mit `arm-none-eabi`-Präfix; optionale Toolchain-Pfade |
| C-Dialekt | `-std=gnu17` |
| Ziel | ARM7TDMI / ARMv4T, Thumb und Interworking |
| ABI-Flag | unter anderem `-mabi=apcs-gnu` — nicht blind fremde ABI-Annahmen übernehmen |
| Modern-Build | `MODERN=1`; `modern` verweist auf `all` |
| Alte Toolchain | `agbcc`-Target meldet seine Deprecation; nicht als Standard verwenden |
| Warnungen | unter anderem `-Wall` und `-Werror` |
| Release-LTO | `USE_LTO_ON_RELEASE ?= 0` in `config.mk` |

Die Installationsdatei enthält geerbte Beispiele mit `pokeemerald.gba` und Speicherverbrauch einer anderen Beispielausgabe. **Für unseren Dateinamen ist das Makefile maßgeblich. Diese Speicherzahlen sind keine Messung unseres SoulGold-Builds.**

### 5.1 Geplante Befehle, noch nicht ausgeführt

Aus dem Repository-Root, nachdem die benötigte Umgebung geprüft und die Durchführung freigegeben wurde:

```bash
# Unveränderter Baseline-Build
make -C soulgold

# Debug-Build nur bei entsprechendem Bedarf
make -C soulgold debug

# Bestehende Zieltests; mGBA-Testwerkzeuge müssen passend verfügbar sein
make -C soulgold check
```

Die Debian-Anleitung nennt `build-essential`, `binutils-arm-none-eabi`, `gcc-arm-none-eabi`, `libnewlib-arm-none-eabi`, `git`, `libpng-dev` und `python3`. Die vollständigen tatsächlich benötigten Werkzeuge sind vor Ausführung aus Buildregeln und Plattformanleitung zu prüfen. Vorhandene Werkzeug-Binaries werden nicht allein wegen ihrer Existenz als passend oder vertrauenswürdig ausgeführt.

**Nicht einmal `make -n` ist hier unsere reine Leseprüfung:** Makefiles können beim Auswerten `$(shell ...)` ausführen. Diese Dokumentation wurde deshalb durch Lesen erstellt, nicht durch einen Make-Aufruf.

### 5.2 Baseline-Nachweise für später

Aufzeichnen: Hauptrepository-Commit, Toolversionen, genaue Flags und Overrides, vollständiges Buildlog, Hash der eigenen Ausgabedatei und tatsächlichen RAM-/ROM-Verbrauch. Der erste funktionierende eigene Baseline-Build ist unsere Referenz für spätere Änderungen, nicht automatisch die offiziell veröffentlichte ROM.

## 6. SoulGold-Speicherformat: besonders geschützter Bereich

**Vanilla-Emerald-Offsets und gewöhnliche Gen-3-Pokémon-Layouts sind hier keine sichere Grundlage.** Dieser Quellstand hat eigene kompakte Pokémon-Strukturen, Speichererweiterungen und Migrationslogik.

### 6.1 Im Quellcode abgesicherte Pokémon-Größen

[`include/pokemon.h`](soulgold/include/pokemon.h) enthält `STATIC_ASSERT`-Prüfungen:

| Struktur / Feld | Erwarteter Wert im Code |
|---|---|
| `sizeof(struct PokemonSecureData)` | 36 Bytes |
| `sizeof(struct BoxPokemon)` | 68 Bytes |
| `offsetof(struct BoxPokemon, secure)` | 32 |
| `sizeof(struct Pokemon)` | 96 Bytes |
| `offsetof(struct Pokemon, legacyCompatibility)` | 68 |
| `offsetof(struct Pokemon, status)` | 76 |

Das sind **Quellcode-Anforderungen**, kein in dieser Session ausgeführter Buildnachweis. Insbesondere darf ein externes Save-Tool mit behaupteten 76-/100-Byte-Strukturen nicht ungeprüft auf diesen Stand angewendet werden.

Vorhandene Zugriffsschnittstellen:

- `GetMonData(...)` ist ein Makro, das nach Argumentanzahl auf `GetMonData2` oder `GetMonData3` verteilt.
- `SetMonData(struct Pokemon *mon, s32 field, const void *dataArg)` erwartet einen Pointer auf passend typisierte Daten.
- `GetBoxMonData(...)` und `SetBoxMonData(...)` betreffen Box-Pokémon.
- `CalculateMonStats(struct Pokemon *mon)` ist deklariert; ob und wann eine Änderung eine Neuberechnung braucht, muss am echten Datenfluss geprüft werden.

Einzelne Felder nicht durch rohe Save-Offsets oder frei erfundene Getter ersetzen. Enum-/Feldkonstanten, erwartete Typen und Implementierung zuerst lesen. Aus dem Namen `secure` allein keine Vanilla-Verschlüsselung ableiten.

### 6.2 SaveBlocks und knappe Reserve

[`src/save.c`](soulgold/src/save.c) sichert unter anderem folgende Werte ab:

| Layout-Anforderung | Wert |
|---|---|
| `sizeof(struct SaveBlock1)` | `0x3C54` |
| `sizeof(struct SaveBlock2)` | `0xB30` |
| `sizeof(struct SaveBlock3)` | `0x64` |
| `SaveBlock1.futureReserved` beginnt bei | `0x3C32` |
| `sizeof(SaveBlock1.futureReserved)` | **34 Bytes** |
| `SaveBlock2.encryptionKey` liegt bei | `0xB4` |
| `SaveBlock1.pokemonStorageExtensionTail` | 1944 Bytes |

`include/config/save.h` beschreibt freigegebene Altspiel-Bereiche und berechnet die Restreserve. Die Rechnung beginnt zwar mit 2048 Bytes, aber **es stehen nicht pauschal 2 KiB frei zur Verfügung**. Der Quellstand erwartet am Ende nur 34 Reservebytes.

`src/save.c` enthält außerdem Legacy-Storage-Formate, Größenprüfungen und Hinweise auf einseitige Konvertierungen. Vor einer Speicheränderung sind aktive Erkennung und Konvertierung vollständig zu lesen; Kommentare allein reichen dafür nicht aus.

### 6.3 Regeln für unseren späteren Auftrag

- Neue Optionen oder Erfolgszustände nicht einfach mitten in bestehende Save-Strukturen einfügen.
- Reservebytes nur nach Beleg ihrer tatsächlichen Verwendung und Anpassung sämtlicher betroffener Assertions belegen.
- Pokémon-, Item-, Attacken-, Trainer-, Flag- und Variablen-IDs stabil halten. Relevante Konstanten liegen in `include/constants/`.
- Gleiches `sizeof` beweist keine semantische Kompatibilität.
- Migration umfasst Layout, ID-Bedeutung und Weltzustand. Bekannte Speicherformate gezielt erkennen; unbekannte nicht still konvertieren.
- Alte eigene Saves nur als Testkopien verwenden; nicht ungefragt ins Repository aufnehmen.
- Für Versionswechsel normale Ingame-Saves verwenden. Save States einer anderen ROM sind keine Kompatibilitätsgrundlage.

**Aktueller Save-Status: ungeprüft.** Weder Altspiel-Kompatibilität noch Kompatibilität zur veröffentlichten SoulGold-ROM wird zugesichert.

## 7. Coding-Regeln, auf unseren Stand angewendet

1. **Datenänderung vor Engine-Neubau prüfen.** Ein Trainerteam gehört zunächst in die `.party`-Quelle; eine Speziesänderung in die tatsächlich verwendete Definition unter `src/data/pokemon/`.
2. **Projekt-Typen verwenden und Breiten prüfen.** Bei Belohnungen, Zählern oder Skalierung vor Multiplikation passend verbreitern und erst nach Begrenzung zurückkonvertieren. Kein generisches `int reward * 2` ungeprüft einbauen.
3. **Bestehende ABI und Layouts respektieren.** Die Makefile-Flags und `STATIC_ASSERT`s sind konkret vorhanden. Ein Host-PC-Test mit anderer Pointerbreite ersetzt keinen Zielbuild.
4. **Strukturpadding und Bitfields beachten.** `BoxPokemon` enthält Bitfields. `packed` ist keine pauschale Lösung für Save-Probleme.
5. **Kein blockierender Code in Tasks oder Menüs.** Rückkehr, Abbruch und Ressourcenfreigabe anhand des existierenden Callback-/Task-Ablaufs planen.
6. **RAM-Budget nachmessen.** Große lokale Arrays belasten den Stack; neue globale Puffer verbrauchen knappen GBA-RAM. Es gibt noch keine belastbare lokale Restbudgetmessung.
7. **Text über Projektformate bearbeiten.** `charmap.txt` und die vorhandene Text-/Script-Pipeline beachten; UTF-8-Text nicht beliebig in ROM-Daten schreiben. Deutsche Übersetzung ist noch kein vereinbartes Ziel.
8. **Grafiken über die vorhandenen Assetregeln bauen.** PNG, Paletten und Tileformate sind unterschiedliche Stufen. Die passende Regel vor einem Assettausch bestimmen.
9. **Keine fremden Binärhooks kopieren.** Uns liegt Quellcode vor. Nur falls ein späterer Auftrag tatsächlich einen Binäreingriff erfordert, dafür einen separaten technischen Plan erstellen.
10. **Keine Nebenprojekte.** Weder Gen-4-Unterstützung noch Engine-Update, Agentenschwarm oder Website-Neubau sind Teil des bisherigen Vorhabens.

## 8. Vorhandene Tests und geplanter Nachweis

Unter `test/` existieren unter anderem `save.c`, `pokemon.c`, `pokemon_storage_system.c`, `gameplay_options.c`, `level_scaling.c`, `hidden_grotto.c`, `achievements.c` und der Ordner `battle/`.

Das Makefile führt `check` und `check-all` über mehrere Test-ELFs aus (`TEST_SHARDS ?= 3`). `check` überspringt bestimmte doppelte Trait-Tests, `check-all` nicht. Die Ergebnisse einzelner Shards sind nicht jeweils das Ergebnis der kompletten Suite. Außerdem enthält `include/config/test.h` abweichende Testkonfigurationen, unter anderem aktivierte Formen. Ein erfolgreicher Testbuild allein beweist deshalb nicht dieselbe Konfiguration wie die normale Spiel-ROM.

| Prüfung für einen späteren Auftrag | Erwarteter Nachweis | Aktuell |
|---|---|---|
| Unveränderter Build | Toolchain, Log, eigene ROM-/ELF-Referenz | Nicht ausgeführt |
| Zielbezogene bestehende Tests | genaue Auswahl, Ergebnisse, übersprungene Fälle | Nicht ausgeführt |
| Neue Regressionstests | positiver Fall, Grenzfall, Abbruch / unverändertes Verhalten | Noch kein Feature gewählt |
| Normaler Spielbuild im Emulator | Start, Feature, Rückkehr, weiterer Spielablauf | Nicht ausgeführt |
| Save-Test | Testkopie laden, spielen, speichern, Neustart | Nicht ausgeführt |
| Patch-Roundtrip | exakte Ausgangsdatei → Patch → identischer eigener Zielhash | Nicht ausgeführt |

Die geeignete `TESTS`-Filterung ist anhand vorhandener Testnamen zu bestimmen. Ein leeres Filterergebnis ist kein bestandener Featuretest. Ohne verfügbare Toolchain oder Emulator verbleibt der Status „nicht getestet“.

## 9. Eigene Dokumentation und spätere Patch-Erstellung

### 9.1 Spieldokumentation ist bereits ein Buildprodukt

[`tools/soulgold_docs/README.md`](soulgold/tools/soulgold_docs/README.md) beschreibt die Pipeline:

- Websitequellen in `docs/src/`, veröffentlichte statische Dateien in `docs/`.
- `python3 tools/soulgold_docs/build_docs.py --static-only` aktualisiert die Oberfläche und Versionsdaten aus bereits veröffentlichten Daten.
- Ein Lauf ohne `--static-only` regeneriert weitere Spieldaten und Routen; Abhängigkeiten und Umfang vorher prüfen.
- `DISPLAY_VERSION` erzeugt Website-Versionsdateien und beeinflusst den Updatehinweis.

Diese Befehle gelten **aus dem Verzeichnis `soulgold/`** und wurden nicht ausgeführt. Nicht zur bloßen Dokumentationspflege unseres Hauptrepositorys starten. Eine Änderung der Versionsanzeige kann gegenüber Spielern eine neue Veröffentlichung behaupten; eigene Versionskennung und Veröffentlichungsweg sind noch zu entscheiden.

### 9.2 Zwei verschiedene Patch-Basen nicht verwechseln

Das Makefile besitzt BPS-Ziele mit `BPS_BASE ?= clean.gba` und `BPS_PATCH ?= soulgold.bps`. Das beschreibt einen Patch gegen die dafür bereitgestellte Basisdatei.

Für uns sind zwei spätere Lieferformen denkbar:

1. **Gesamtpatch:** exakt identifizierte saubere Emerald-Basis → unsere SoulGold-Version.
2. **Zusatzpatch:** exakt identifizierte bestehende SoulGold-ROM → unsere persönliche Variante.

Der Makefile-Standard entscheidet nicht automatisch, welche dieser Varianten du möchtest. Basisdatei, Hash und Save-Anforderungen müssen vor Erstellung feststehen. Keine ROM-Datei oder private Saves ungefragt committen. Die vorhandenen Ignore-Regeln unterstützen das; erzwungenes Hinzufügen würde sie allerdings umgehen.

## 10. Ablauf für die nächste KI-Arbeitssession

### Phase A — Wunsch präzisieren

Festlegen: gewünschter Effekt, betroffener Spielabschnitt, Nicht-Ziele, Spielstandanforderungen und ob unser lokaler Quellstand als Basis akzeptiert wird.

### Phase B — belegten Änderungsplan erstellen

Für genau diesen Wunsch:

1. Definition, Aufrufer, Datenquellen und Tests auffinden.
2. Auslöser → Verarbeitung → Anzeige → Persistenz beschreiben.
3. Prüfen, ob vorhandene Einstellung oder Datenänderung genügt.
4. Minimal betroffene Dateien nennen; generierte Dateien unterscheiden.
5. Speicher-, Save-, ID- und Balancerisiken benennen.
6. Abnahmetests mit erwarteten Ergebnissen und Rollbackplan formulieren.
7. Offene Entscheidungen vor Umsetzung zurückfragen.

### Phase C — nur nach Freigabe implementieren

Aktuellen Branch und lokale Änderungen prüfen, Baseline herstellen, kleinen Eingriff umsetzen, Tests tatsächlich durchführen und getrennt dokumentieren. Keine fremden Änderungen überschreiben, keine automatischen Upstream-Updates und kein eigenmächtiger Merge.

Die vollständige Einbindung erlaubt direkte Commits im Hauptrepository. Ein eigener Fork oder Submodul-Commit ist dafür nicht erforderlich. Für spätere Pushes und PRs gelten jeweils der ausdrückliche Auftrag und die Regeln der Arbeitsumgebung. Die bereits erfolgte Erlaubnis zur Quellcodeübernahme ist keine dauerhafte Erlaubnis für alle weiteren Veröffentlichungen oder Connector-Zugriffe.

### Stopkriterien

- Gewünschte Funktion fehlt im lokalen Stand, obwohl sie laut Release erwartet wird.
- Voraussetzung wäre ein anderer Quellstand oder ein Engine-Upgrade.
- Save-Layout oder ID-Semantik müsste ohne geklärte Kompatibilitätsentscheidung verändert werden.
- Baseline baut nicht oder relevante Ausgangstests scheitern bereits.
- Tatsächlicher Umfang überschreitet den freigegebenen Auftrag.

## 11. Vorlage: unser nächster konkreter Änderungsauftrag

Noch keine Inhalte erfinden; gemeinsam ausfüllen:

```text
Projekt: SoulGold unter soulgold/
Herkunft: Tag 1.2.1 / e73803309e78231142160b3e1029df884bc8b5f1
Bekannte Einschränkung: Quellstand laut Upstream hinter veröffentlichtem Spiel

Lokalen Quellstand als Basis akzeptiert: OFFEN
Gewünschte Änderung: OFFEN
Sichtbares Verhalten vorher / nachher: OFFEN
Betroffene Spielsituationen: OFFEN
Nicht-Ziele: OFFEN
Vorhandene eigene SoulGold-ROM / Version: OFFEN
Bestehenden Spielstand erhalten: OFFEN
Eigene Versionskennung: OFFEN
Spätere Lieferform (nur Quellcode / Gesamtpatch / Zusatzpatch): OFFEN

Nach gezielter Analyse ergänzen:
- Belegte Symbole und Dateien
- Datenquelle und Generierungsweg
- Minimaler Implementierungsplan
- Save-/ID-/Speicher-Risiken
- Konkrete Abnahmetests
- Rollback und verbleibende Fragen

Implementierungsfreigabe: AUSSTEHEND
Build- und Testergebnisse: NOCH NICHT VORHANDEN
```

## 12. Maßgebliche Quellen und Pflege

Die lokalen Links und Pfade in diesem Dokument beziehen sich auf unseren übernommenen Quellstand. Vorrangige Belege sind Code, Buildregeln und Tests dieses Stands, nicht allgemeine Tutorials oder frühere KI-Aussagen. Lokale Upstream-Dokumentation kann geerbt oder veraltet sein; Abweichungen zum Code sind oben ausdrücklich gekennzeichnet.

Externe Herkunftsreferenzen:

- [Upstream-Repository](https://github.com/Eemeliri/soulgold)
- [Herkunftscommit](https://github.com/Eemeliri/soulgold/commit/e73803309e78231142160b3e1029df884bc8b5f1)
- [Release-Seite 1.2.1](https://github.com/Eemeliri/soulgold/releases/tag/1.2.1)

Nach einer späteren Änderung hier nur tatsächlich bestätigte Erkenntnisse nachtragen. Tests mit Datum, Quellstand und Ergebnis erfassen. Allgemeine Möglichkeiten nicht als vorhandene SoulGold-Funktionen darstellen.

**Nächster Schritt:** Wir formulieren deinen gewünschten Effekt. Danach erstellen wir die konkrete, belegte Änderungsliste — noch nicht umgekehrt.

## 13. Separates Shaderpaket — jetzt übernommen

Auf Nutzerauftrag liegen ScaleFX, Bevel und Image Adjustment samt ihren benötigten Dateien direkt unter `shaders/upstream/`. Herkunft: `libretro/slang-shaders`, Commit `2345ee91602a7404d3a1a6a5df6108d7305fdad4`. Kein Submodul; kein vollständiger Import der unbenötigten übrigen Sammlung.

Das minimale gemeinsame Preset heißt `shaders/soulgold-vivid-relief.slangp`: ScaleFX → Bevel → Image Adjustment. Startwerte: `BEVEL_LEVEL = 0.10`, `ia_saturation = 1.20`. Keine Emulator-Konfiguration enthalten. Die Shader sind separate Host-Effekte, keine Änderung der GBA-ROM.

Die 12 übernommenen Dateien wurden bytegenau mit den Upstream-Git-Blobs verglichen. Fünf statische Tests für Hashes, Abhängigkeiten, Preset-Verknüpfung und Parameter sind bestanden. Keine Shaderkompilierung, GPU-Ausführung oder visuelle Abnahme. Lizenzhinweise einschließlich GPL-Header-Abhängigkeit von Image Adjustment stehen in `shaders/licenses/README.md`. Weitere Details in `shaders/README.md`.

Separat vorgemerkt: Einen der neun Starter durch Mew ersetzen; aktiven Auswahlpfad und Slot vor Umsetzung bestimmen. Dieser Auftrag wurde mit der Shaderübernahme nicht ausgeführt.
