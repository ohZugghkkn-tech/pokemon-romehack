# Pokémon-ROM-Hacks: Technik, Code und eigene Updates

Diese Notizen führen die bisherigen Erklärungen zusammen: Wie Pokémon-ROM-Hacks auf PC-Emulatoren funktionieren, wie der zugrunde liegende Code aufgebaut ist und wie du einen vorhandenen Hack für dich selbst erweitern kannst. Die Beispiele sind überwiegend auf Game Boy Advance (GBA) bezogen; Unterschiede zu Game Boy und Nintendo DS werden gesondert erklärt.

> Codebeispiele sind, sofern nicht anders angegeben, vereinfachte Veranschaulichungen. Funktionsnamen, Dateipfade, Datenstrukturen und Build-Befehle können je nach Projekt und Version abweichen.

## 1. Was ist ein ROM-Hack?

Eine ROM-Datei enthält das Programm und die Spieldaten eines Konsolenspiels. Ein ROM-Hack verändert diese Inhalte, etwa:

- Pokémon, Attacken, Fähigkeiten und Werte;
- Trainerteams und Schwierigkeitsgrad;
- Karten, Dialoge und Story;
- Grafiken, Musik und Menüs;
- Kampfregeln und andere Engine-Funktionen.

Ein PC-Emulator führt nicht plötzlich ein gewöhnliches Windows-Spiel aus. Er bildet die ursprüngliche Konsole nach und führt deren Maschinenbefehle aus. Ein GBA-Hack bleibt also ein GBA-Programm, auch wenn du ihn auf dem PC spielst.

Beispiele für Emulatoren sind mGBA für GBA, SameBoy für Game Boy/Game Boy Color und melonDS für Nintendo DS. Welche Funktionen und Patchformate unterstützt werden, hängt vom Emulator und dessen Version ab.

## 2. Zwei Wege zum ROM-Hacking

### 2.1 Binary Hacking: eine fertige ROM bearbeiten

Du veränderst die bereits kompilierten Bytes einer `.gba`, `.gb` oder `.nds`.

```text
Fertige ROM
    ↓
Daten / Texte / Scripts / Maschinenbefehle ändern
    ↓
Veränderte ROM
```

Bei GBA sind beispielsweise HexManiacAdvance, ältere Werkzeuge wie AdvanceMap und XSE sowie Erweiterungsprojekte wie CFRU und DPE relevant. CFRU steht für Complete FireRed Upgrade, DPE für Dynamic Pokémon Expansion.

Werkzeuge helfen dabei, Bytebereiche als sinnvolle Daten darzustellen: etwa als Trainerteam, Pokémon-Werte oder Karten. Das funktioniert aber nur, wenn sie die jeweiligen Datenstrukturen und Positionen ausreichend kennen.

Bei stark veränderten Hacks können Daten verschoben, erweitert oder neu organisiert sein. Ein Tool, das das Originalspiel unterstützt, unterstützt deshalb nicht automatisch jeden darauf basierenden Hack.

### 2.2 Decompilation und Disassembly: aus Quellcode bauen

Bei einem Decomp-Projekt liegt rekonstruierter Quellcode vor. Bei einer Disassembly liegt das Spiel hauptsächlich als lesbarer Assemblercode vor. Unveränderte, passende Projektstände können die Original-ROM bytegenau reproduzieren; dafür müssen unter anderem Version und Toolchain passen.

```text
Quellcode + Daten + Grafiken + Musik
                 ↓
Compiler / Assembler / Linker / Asset-Werkzeuge
                 ↓
Neue ROM
```

Beispiele:

| Generation | Beispiele | Typische technische Grundlage |
|---|---|---|
| Gen 1–2 | `pret/pokered`, `pret/pokecrystal` | SM83-/Game-Boy-Assembler, RGBDS |
| Gen 3 | `pret/pokefirered`, `pret/pokeemerald` | C und ARM-/Thumb-Assembler |
| Gen 3, erweitert | `rh-hideout/pokeemerald-expansion` | Erweiterte Emerald-Codebasis |
| Gen 4 | `pret/pokeplatinum` | C, Assembler, DS-Dateisystem und Overlays |

Für GBA kommen je nach Projekt `agbcc` oder eine moderne ARM-GCC-Toolchain zum Einsatz. Häufig steuert `make` den Build. Für Gen-1-/Gen-2-Projekte heißen die aktuellen zentralen RGBDS-Werkzeuge `rgbasm`, `rgblink` und `rgbfix`.

**Wichtig:** Ein Decomp-Projekt lädt deine beliebige fertige Hack-ROM nicht automatisch wieder als ursprüngliches C-Projekt. Wenn du einen vorhandenen Hack weiterentwickeln möchtest, brauchst du idealerweise dessen eigenen Quellcode und nicht nur den des ursprünglichen Pokémon-Spiels.

## 3. Was ein GBA-Emulator technisch nachbildet

Der GBA verwendet einen ARM7TDMI-Prozessor mit ungefähr 16,78 MHz. Er unterstützt ARM- und Thumb-Befehle. Thumb verwendet überwiegend kompakte 16-Bit-Befehle; ARM überwiegend 32-Bit-Befehle.

Vereinfachte Speicherübersicht:

| Adresse / Bereich | Bedeutung |
|---|---|
| `0x00000000` | BIOS, 16 KiB |
| `0x02000000` | EWRAM, 256 KiB |
| `0x03000000` | IWRAM, 32 KiB |
| `0x04000000` | Hardware- und I/O-Register |
| `0x05000000` | Farbpaletten |
| `0x06000000` | VRAM, 96 KiB |
| `0x07000000` | OAM, 1 KiB; Einträge für bis zu 128 Hardware-Sprites |
| `0x08000000–0x09FFFFFF` | Primäres Game-Pak-ROM-Fenster, bis zu 32 MiB |
| `0x0E000000` | Adressbereich für bestimmte Cartridge-Speicher wie SRAM/Flash |

Daneben existieren weitere ROM-Fenster mit anderen Waitstates. EEPROM hat eine andere Zugriffstechnik; nicht jeder Speichertyp benutzt einfach denselben Bereich.

Der Emulator bildet CPU, Speicherzugriffe, Grafik, Sound, Eingaben, Interrupts und Cartridge-Speicher nach. Der Hack muss weiterhin mit den Grenzen dieser emulierten Hardware zurechtkommen.

## 4. Wie ein GBA-Pokémon-Projekt aufgebaut ist

Typische Verzeichnisse in Decomp-Projekten:

```text
src/       C-Implementierungen
include/   Header, Konstanten und Strukturen
asm/       Assemblercode
data/      Tabellen und Scripts
graphics/  Grafikquellen
sound/     Musik und Sounddaten
```

Die genaue Aufteilung unterscheidet sich zwischen FireRed, Emerald und Erweiterungsprojekten.

### 4.1 Hauptschleife, Callbacks und Tasks

Ein Spiel läuft fortlaufend durch eine Hauptschleife. In Gen-3-Projekten sind unter anderem `AgbMain()`, `gMain.callback2`, `SetMainCallback2()` und `RunTasks()` wichtige Begriffe.

Vereinfachtes Prinzip:

```c
// Schematisch: keine vollständige Originalimplementierung.
while (1)
{
    ReadInput();
    RunCurrentGameCallback();
    WaitForVBlank();
}
```

Der aktuelle Callback bestimmt beispielsweise, ob gerade Oberwelt, Menü oder Kampf aktualisiert wird. Tasks ermöglichen kleine, kooperativ ausgeführte Abläufe; sie sind keine gewöhnlichen Betriebssystem-Threads. Welche Callbacks Tasks ausführen, hängt vom jeweiligen Spielzustand ab.

VBlank ist die Zeit zwischen den sichtbaren Bildaufbauten. Das Spiel nutzt sie unter anderem für geeignete Grafikübertragungen und Registeraktualisierungen.

### 4.2 Pokémon und Attacken als Daten

Viele Änderungen sind Tabellenänderungen und keine komplett neue Spiellogik.

```c
// Vereinfachtes Beispiel.
struct SpeciesInfo
{
    unsigned char baseHP;
    unsigned char baseAttack;
    unsigned char baseDefense;
};

const struct SpeciesInfo exampleSpecies =
{
    .baseHP = 45,
    .baseAttack = 49,
    .baseDefense = 49,
};
```

In echten Projekten findest du je nach Codebasis beispielsweise `gBaseStats`, `gSpeciesInfo`, `struct BaseStats`, `struct SpeciesInfo` oder Makros wie `LEVEL_UP_MOVE(...)`.

Eine Änderung am Basis-Angriff betrifft zunächst die Speziesdaten. Ob die Werte eines bereits vorhandenen Pokémon sofort neu berechnet werden, hängt vom jeweiligen Codepfad ab.

### 4.3 Event-Scripts: eine kleine Sprache innerhalb des Spiels

Dialoge, NPC-Ereignisse und Storyfortschritt werden häufig durch Scripts gesteuert.

```text
Spieler spricht NPC an
         ↓
Script beginnt
         ↓
Flag prüfen → Text anzeigen → Gegenstand geben → Flag setzen
```

Das Spiel interpretiert dafür Bytecode. Ein `ScriptContext` verwaltet den Ablauf; eine Tabelle wie `gScriptCmdTable` ordnet Befehlen passende C-Funktionen zu.

Typische Bestandteile:

- `ScrCmd_*`: Implementierungen von Scriptbefehlen;
- `gSpecials`: aufrufbare C-Spezialfunktionen;
- Flags: boolesche Zustände, etwa „Geschenk schon erhalten“;
- Variablen: Zahlenwerte für Storyzustände oder Zwischenergebnisse;
- `gSaveBlock1Ptr`: Zugriff auf einen Teil der gespeicherten Spielinformationen.

Die genaue Bedeutung numerischer Opcodes und Variablenbereiche ist spiel- und versionsabhängig. Werte dürfen nicht blind zwischen Hacks übertragen werden.

Werkzeuge wie Poryscript können eine angenehmere Scriptsprache in die für das Projekt benötigten Scriptdateien übersetzen. Porymap hilft beim Bearbeiten von Karten und Ereignissen.

### 4.4 Kampflogik

Auch der Kampf verwendet in Gen-3-Spielen Script- und Dispatch-Systeme. Begriffe sind beispielsweise `gBattleScriptingCommandsTable` sowie Befehle für Schadensberechnung, Typenwirkung oder kritische Treffer.

```text
Attacke auswählen
      ↓
Kampfscript abarbeiten
      ↓
Treffer / Schaden / Typenwirkung / Effekte verarbeiten
      ↓
Animationen und Zustände aktualisieren
```

Ein neues Kampffeature kann mehrere Bereiche berühren: Daten, C-Code, Scripts, Animationen und Benutzeroberfläche.

## 5. Pointer, Offsets und C-Injection

### 5.1 Dateioffset ist nicht gleich CPU-Adresse

Angenommen, Daten stehen in der ROM-Datei am Offset `0x24F050`. Im primären GBA-ROM-Fenster entspricht das üblicherweise:

```text
0x08000000 + 0x0024F050 = 0x0824F050
```

Ein 32-Bit-Pointer auf diese Adresse wird im Little-Endian-Format so gespeichert:

```text
50 F0 24 08
```

Nicht jeder Zahlenwert in der ROM ist aber ein solcher Pointer. Es gibt auch relative Offsets, Indizes und andere Formate.

### 5.2 Repointing

Wenn eine Tabelle oder ein Text länger wird, reicht der bisherige Platz eventuell nicht aus. Dann kannst du die Daten an eine geeignete andere Stelle verschieben und die Verweise darauf ändern.

```text
Alter Pointer → alte kleine Tabelle

Neuer Pointer → neue größere Tabelle
```

Mit `0xFF` gefüllte Bereiche sind ein möglicher Hinweis auf freien Platz, aber kein Beweis. Ohne Prüfung kannst du wichtige Inhalte überschreiben. Außerdem müssen Länge, Ausrichtung und alle relevanten Referenzen stimmen.

### 5.3 C-Injection und Hooks

Bei Binary Hacking kann eigener C-Code für die GBA-CPU kompiliert und in die ROM eingefügt werden. Ein Hook leitet einen bestehenden Programmablauf zur neuen Routine um.

```text
Bestehender Code → Hook → eigene Routine → Rückkehr
```

Dabei müssen unter anderem Register, Stack, Aufrufkonvention, überschriebenen Befehle und Sprungreichweiten berücksichtigt werden.

Bei Funktionsadressen für Thumb-Interworking kennzeichnet das niederwertigste Bit den Thumb-Modus. Deshalb begegnet dir bei passenden indirekten Aufrufen häufig eine Adresse mit gesetztem Bit 0, also sinngemäß `Adresse + 1`. Das ist keine allgemeine Vorschrift, bei jeder ROM-Adresse einfach eins zu addieren.

## 6. Unterschiede zu Game Boy und Nintendo DS

### Game Boy / Game Boy Color

Gen-1-/Gen-2-Projekte verwenden hauptsächlich Assembler für den SM83-Prozessor. Der Begriff „GB-Z80“ wird gelegentlich verwendet, obwohl der Prozessor kein vollständiger Z80 ist.

ROM-Banking ist wichtig: Ein Bereich bleibt normalerweise auf Bank 0 abgebildet, während ein anderer 16-KiB-Bereich zwischen ROM-Bänken umgeschaltet werden kann. Ein Pointer allein reicht deshalb nicht immer aus; der Bankkontext ist entscheidend.

Datentabellen werden häufig mit Assembler-Direktiven wie `db` für Bytes definiert.

### Nintendo DS

Eine `.nds` enthält nicht nur eine flache Sammlung von GBA-artigen Tabellen. Typische Bestandteile sind:

- ARM9- und ARM7-Programme;
- ein internes Dateisystem;
- `.narc`-Archive mit Daten und Ressourcen;
- Overlays, also zur Laufzeit geladene Programmteile.

Werkzeuge wie DSPRE und Projekte wie `pret/pokeplatinum` oder `hg-engine` betreffen unterschiedliche Aspekte dieses Umfelds. Ein GBA-Werkzeug ist nicht automatisch für einen DS-Hack geeignet.

## 7. ROM-Hacks als Patches

Ein Patch beschreibt, wie aus einer genau bestimmten Ausgangsdatei eine Zieldatei entsteht. Für die Anwendung brauchst du die richtige Ausgangsversion.

| Format | Eigenschaften |
|---|---|
| IPS | Einfach, klassisch; 24-Bit-Offsets, keine eingebaute Ausgangsdatei-Prüfsumme |
| UPS | Unterstützt größere Dateien und CRC32-Prüfungen |
| BPS | Unterstützt Prüfsummen und effiziente Kopieroperationen |
| xdelta | Häufig bei größeren Dateien und DS-Hacks verwendet |

Das klassische IPS-Format beginnt mit `PATCH`. Datensätze enthalten einen 3-Byte-Offset und eine 2-Byte-Länge; bei Länge null folgt ein RLE-Datensatz. `EOF` markiert das Ende. Die 24-Bit-Adressierung begrenzt die direkt adressierbaren Startpositionen auf den Bereich unter 16 MiB; für größere GBA-ROMs sind andere Formate meist geeigneter.

BPS kann insbesondere auch Daten aus der Ausgangsdatei oder bereits erzeugten Zielbereichen kopieren. Prüfsummen helfen, eine falsche Ausgangsdatei zu erkennen.

Patches werden beispielsweise mit Floating IPS, NUPS, Rom Patcher JS oder xdelta-Werkzeugen verarbeitet. Emulator-Softpatching ist abhängig vom Emulator und Format.

Ein Patch ist ein übliches Distributionsformat, aber nicht automatisch eine Garantie für rechtliche Unbedenklichkeit. Veröffentliche keine vollständigen fremden ROM-Dateien; beachte außerdem Lizenzen und Rechte an Code und Assets.

## 8. Einen vorhandenen ROM-Hack für dich selbst updaten

**Ja: Du kannst einen vorhandenen Hack verändern und daraus deine persönliche Version erstellen.** Der wichtigste Unterschied ist, ob du den Quellcode oder nur die fertige ROM besitzt.

### 8.1 Mit dem Quellcode des konkreten Hacks

```text
Quellcode des vorhandenen Hacks
              ↓
Eigene Änderungen an Code / Daten / Maps
              ↓
Kompilieren
              ↓
Deine persönliche neue Version
```

Der normale Emerald- oder FireRed-Quellcode enthält nicht automatisch die Änderungen des Hacks. Du brauchst idealerweise den passenden Projektstand des konkreten Hacks und dessen Build-Anleitung.

Beispiel einer eigenen Regel:

```c
// Vereinfachtes Beispiel, kein direkt einsetzbarer Projektcode.
int CalculateReward(int normalReward)
{
    return normalReward * 2;
}
```

Damit diese Regel wirkt, muss der tatsächliche Belohnungsablauf sie verwenden. Außerdem sind Datentypen, Obergrenzen und Sonderfälle zu prüfen.

Empfohlenes Vorgehen:

1. Hack-Version und zugehörigen Quellcode-Stand bestimmen.
2. Build-Anleitung und Lizenz lesen.
3. Erst einen unveränderten Build erfolgreich erstellen und testen.
4. Eine kleine Änderung umsetzen.
5. Neu bauen und gezielt testen.
6. Änderungen mit Versionsverwaltung und kurzen Notizen nachvollziehbar halten.

### 8.2 Nur mit der fertigen ROM

Dann bearbeitest du die kompilierten Daten und gegebenenfalls Maschinenbefehle.

| Gewünschte Änderung | Typischer Ansatz |
|---|---|
| Andere Basiswerte für ein Pokémon | Datentabelle bearbeiten |
| Anderes Trainerteam | Trainerdaten bearbeiten |
| Anderer NPC-Text | Text, Pointer und gegebenenfalls Script bearbeiten |
| Neues Menü oder neue Kampfmechanik | Quellcode oder aufwendige Analyse und Code-Injection |

HexManiacAdvance kann bei unterstützten GBA-Strukturen hilfreich sein. Bei erweiterten Hacks können zusätzliche Metadaten, Tabellenbeschreibungen oder manuelle Analysen erforderlich sein.

Aus der fertigen ROM erhältst du nicht einfach wieder den ursprünglichen, sauber kommentierten C-Code. Disassembler und andere Reverse-Engineering-Werkzeuge helfen bei der Analyse, ersetzen aber nicht automatisch das Originalprojekt.

### 8.3 Eigenen Zusatzpatch erstellen

Du kannst einen Patch erstellen, dessen Ausgangsdatei bereits der vorhandene Hack ist:

```text
Vorhandener Hack, Version 1.0
              +
Dein persönlicher Zusatzpatch
              =
Hack 1.0 mit deinen Änderungen
```

Beispiel mit Floating IPS:

```bash
flips --create --bps hack-v1.gba hack-meine-version.gba mein-update.bps
```

Die Basis ist hier ausdrücklich `hack-v1.gba`, nicht die unveränderte originale Pokémon-ROM.

Anwenden und prüfen:

```bash
flips --apply mein-update.bps hack-v1.gba test-ergebnis.gba
```

Vergleiche anschließend `test-ergebnis.gba` byteweise oder per Hash mit `hack-meine-version.gba`. Sie müssen identisch sein.

Dokumentiere mindestens:

- Name und genaue Version des benötigten Hacks;
- Prüfsumme der Ausgangsdatei, beispielsweise SHA-256;
- Liste deiner Änderungen;
- getesteten Emulator;
- Hinweise zur Spielstand-Kompatibilität.

### 8.4 Spätere offizielle Updates des Hacks

Dein Zusatzpatch ist kein automatisches System, das jede zukünftige Version versteht.

Mit Quellcode kannst du Änderungen später zusammenführen, musst aber gegebenenfalls Konflikte lösen. Bei direkten ROM-Änderungen können Tabellen, Funktionen und Pointer inzwischen an anderen Positionen liegen.

```text
Deine Änderungen auf Version 1.0
              +
Offizielle Version 1.1
              ↓
Änderungen prüfen, übertragen und erneut testen
```

Auch Updates einer zugrunde liegenden Engine wie pokeemerald-expansion können Anpassungen erfordern. Folge dabei der Update-Anleitung des konkreten Projektstands; manche Versionen empfehlen Zwischenschritte statt eines sehr großen Versionssprungs.

## 9. Spielstände und Save States

### 9.1 Normaler Spielstand und Emulator-Schnellspeicher sind verschieden

- Ein normaler Ingame-Spielstand speichert die vom Spiel vorgesehenen Daten, auf dem PC oft in einer `.sav`-Datei.
- Ein Save State hält einen Emulatorzustand fest, etwa RAM, CPU-Register und weitere Hardwarezustände.

Ein Save State einer alten ROM-Version kann mit einer neuen ROM-Version problematisch sein. Für Updates ist ein regulärer Ingame-Spielstand die bessere Grundlage, sofern der Hack dessen Kompatibilität unterstützt.

### 9.2 Was alte Spielstände gefährdet

Beispiele:

- verändertes Layout von `SaveBlock1` oder `SaveBlock2`;
- verschobene oder neu belegte gespeicherte Felder;
- andere Bedeutungen gespeicherter Pokémon-, Item- oder Attacken-IDs;
- umgenutzte Storyflags und Variablen;
- geänderte Karten und Ereignisse am gespeicherten Aufenthaltsort.

Eine erfolgreiche Prüfsumme beweist nicht, dass die neue Version die alten Daten semantisch richtig interpretiert.

### 9.3 Sichere Update-Routine

1. ROM und normalen Spielstand separat sichern.
2. Wenn möglich, in der alten Version regulär im Spiel speichern und den Emulator schließen.
3. Die neue ROM in einer Testkopie öffnen.
4. Den normalen Spielstand gemäß Emulator-Konfiguration laden; bei vielen Emulatoren muss der Basisdateiname passen.
5. Team, Items, Storyfortschritt, Kartenübergänge und Speichern/Laden prüfen.
6. Alte ROM und alte Saves behalten, bis die neue Version ausreichend getestet ist.

Wenn du selbst das Speicherformat änderst, brauchst du gegebenenfalls eine explizite Migration oder musst klar einen neuen Spielstand voraussetzen. Ein Versionsfeld und eine Konvertierungsroutine sind mögliche Designbausteine, müssen aber sorgfältig implementiert werden.

## 10. Praktischer Einstieg für dein eigenes Vorhaben

Bevor konkrete Änderungen gemacht werden, sind diese Angaben wichtig:

1. **Welcher Hack?** Name und genaue Version.
2. **Welche Plattform?** `.gb`, `.gbc`, `.gba` oder `.nds`?
3. **Was soll sich ändern?** Zum Beispiel Trainer, Werte, Text, Karten oder neue Mechanik.
4. **Ist der Quellcode verfügbar?** Falls ja: welcher Projektstand?
5. **Muss dein vorhandener Spielstand weiter funktionieren?**

Als erster Versuch eignet sich eine einzelne kleine Änderung mit einem klaren Test. Eine neue Kampfmechanik oder ein komplett neues Menü ist deutlich aufwendiger als ein geänderter Tabellenwert.

## 11. Quellen und weiterführende Links

Die bisherigen Erklärungen stützten sich unter anderem auf folgende Recherchequellen. Community-Beiträge und Dokumentation können ältere Werkzeugstände beschreiben; maßgeblich bleibt die Dokumentation des konkreten Projekts.

### Architektur und Code

- [pokefirered: Architekturübersicht](https://deepwiki.com/pret/pokefirered)
- [pokefirered: Event-Scripting-System](https://deepwiki.com/pret/pokefirered/4.3-event-scripting-system)
- [pokefirered: Speicherlayout und Linkerscripts](https://deepwiki.com/pret/pokefirered/10.4-memory-layout-and-linker-scripts)

### Vorhandene Hacks bearbeiten

- [Simple Gen 3 Hacking Guide with Hex Maniac Advance](https://www.pokecommunity.com/threads/simple-gen-3-hacking-guide-with-hex-maniac-advance.537893/)
- [DPE-erweiterte Evolutionstabellen in HexManiacAdvance bearbeiten](https://www.pokecommunity.com/threads/how-to-get-dpe-expanded-evolution-table-into-hexmaniacadvance-for-quick-easy-edits.444937/)
- [Binary Hacking und Decomp im Vergleich](https://www.pokecommunity.com/threads/can-binary-and-decomp-work-in-tandem-without-much-issue.498575/)
- [Diskussion: Pokémon-Werte in einem vorhandenen Hack bearbeiten](https://www.pokecommunity.com/threads/i-want-to-edit-stats-of-pokemons-in-an-existing-rom-hack-radical-red.445272/)

### Patches, Updates und Kompatibilität

- [Patch-Dateien erstellen: Übersicht](https://www.bjsgamevault.com/blogs/news/create-rom-hack-patch-files)
- [Floating-IPS- und xdelta-Befehlsbeispiele](https://tech-insider.org/rom-patcher-ips-bps-xdelta-windows-13-steps-2026/)
- [Konkretes Beispiel für Risiken geänderter Save-Strukturen](https://github.com/MinimalEffort07/pokefirered/issues/139)
- [pokeemerald-expansion-Fork mit Hinweisen zum Aktualisieren](https://github.com/GarnetTheWolf/pokeemerald-expansion)

---

**Kurz gesagt:** Ein eigener Update-Hack ist möglich. Mit dem Quellcode des vorhandenen Hacks ist saubere Weiterentwicklung meist wesentlich einfacher. Mit nur der ROM sind Datenänderungen oft machbar, neue Engine-Funktionen aber deutlich aufwendiger. Sichere immer deine Ausgangsversion und deinen Spielstand und behandle jede neue Version als eigene, zu testende Grundlage.

## 12. Lückenprüfung und Status dieser Planung

**Stand: 9. November 2026. Dieser Zusatz ist ein Planungs- und Übergabedokument für spätere KI-Arbeitssessions, keine bereits umgesetzte ROM-Änderung.**

Die Grundlagen oben erklären die Architektur, reichen aber noch nicht für einen sicheren Implementierungsauftrag. Insbesondere fehlen bisher konkrete Projektidentität, nachvollziehbare Codebelege, ABI-/Datenlayout-Prüfungen und reproduzierbare Tests.

| Erkannte Lücke | Ergänzung / Konsequenz |
|---|---|
| Kein konkreter Hack und Versionsstand gewählt | Vor Umsetzung Ausgangsdatei bzw. Quellstand eindeutig identifizieren |
| Beispielnamen könnten als echte APIs missverstanden werden | Jede Funktion im Zielprojekt nachweisen; Beispiele nicht blind einfügen |
| C-Typen, Überläufe und Strukturpadding kaum erklärt | Regeln und Beispiel in Abschnitt 14 |
| Build-Erfolg mit funktionierendem Spiel verwechselt | Baseline, Hosttests und Emulatortests getrennt bewerten |
| Hooks ohne nachgewiesene Aufrufkonvention | Register, Instruktionen und Rückkehradresse vor Eingriff analysieren |
| Save-Kompatibilität nur allgemein beschrieben | Binärlayout, ID-Semantik und Migration getrennt prüfen |
| Keine klare Übergabe zwischen KI-Sessions | Auftragsschablone, Belegpflicht und Stopkriterien ergänzen |
| Quellen sind teilweise Sekundärtexte und ältere Forenbeiträge | Projektquellcode und passende Tool-Dokumentation als stärkere Nachweise verwenden |

### 12.1 Was aus unserem Chat feststeht

- Zielrichtung: einen vorhandenen Pokémon-ROM-Hack für den eigenen Gebrauch erweitern.
- Plattformkontext: Spielen mit einem PC-Emulator; konkrete Konsolengeneration noch offen.
- Aktuell planen und dokumentieren wir nur. Es gibt noch keinen freigegebenen Implementierungsauftrag.
- Name und Version des Hacks, gewünschtes Feature, Quellcode-Verfügbarkeit und Save-Anforderungen sind noch offen.
- Für den GitHub-Connector wurde keine Erlaubnis erteilt. Dieses Dokument erteilt weder dafür noch für Downloads, Uploads, Veröffentlichungen oder Repository-Eingriffe eine neue Freigabe.
- Bei Erstellung dieses Zusatzes wurde kein Ziel-Hack untersucht oder gebaut. Die neuen Coding-Hinweise sind allgemeines Fachwissen, keine frisch verifizierten Aussagen über ein bestimmtes Projekt.

**Wissensstatus:** „im Chat erklärt“ bedeutet nicht „am Ziel-Hack bestätigt“. Ein erfolgreicher späterer Test muss mit Version, Vorgehen und Ergebnis dokumentiert werden.

## 13. Vor Implementierung: Identität und technische Bestandsaufnahme

Eine spätere Arbeitssession soll zuerst einen kurzen Befund erstellen, ohne bereits Änderungen vorzunehmen:

1. Hackname, Release, Sprache und Plattform feststellen.
2. Ausgangs-ROM über Dateigröße und SHA-256 identifizieren; Dateiname allein reicht nicht.
3. Falls Quellcode vorliegt: Commit-ID, lokale Änderungen, Konfiguration, Submodule und benötigte Assets erfassen.
4. Toolchain und Build-Anleitung dem passenden Projektstand zuordnen. Keine aktuelle Anleitung ungeprüft auf einen alten Stand anwenden.
5. Prüfen, ob dieser Quellstand tatsächlich zum gewünschten Release gehört. Eine selbst gebaute ROM muss nicht automatisch dessen Hash treffen; Abweichungen erklären, nicht ignorieren.
6. Lizenzlage und Zugangsberechtigungen klären. Keine fremden ROMs, BIOS-Dateien oder privaten Spielstände ungefragt beschaffen oder veröffentlichen.
7. Erst nach gesondertem Auftrag einen unveränderten Baseline-Build und dessen Tests durchführen.

Geplante Nachweise sind beispielsweise eine Toolversionsliste, Buildlog, ROM-Hash und eine Linker-Map. Eine Map ordnet Symbole Speicherbereichen zu; eine ELF-Datei kann zusätzlich Symbole und Debug-Informationen enthalten. Die finale `.gba` enthält diese Informationen normalerweise nicht vollständig.

**Matching-Build und Modern-Build sind unterschiedliche Ziele:** Ein unverändertes Matching-Projekt kann bytegenaues Reproduzieren anstreben. Nach Featureänderungen ist Gleichheit zur Original-ROM gerade nicht zu erwarten. Dann zählen reproduzierbarer eigener Build und nachgewiesenes Verhalten.

## 14. C-Coding-Wissen für die spätere Umsetzung

### 14.1 Datentypen, Überläufe und Rundung

- `u8`, `u16`, `u32` sind häufig Projekt-Typaliase; Definitionen vor Verwendung lesen.
- Nicht voraussetzen, dass Host-PC und Zielkonsole dieselben Größen für Pointer, `long` oder Strukturen verwenden.
- Vor einer Multiplikation in einen ausreichend breiten Typ umwandeln. Eine nachträgliche Umwandlung repariert einen bereits entstandenen Überlauf nicht.
- Signed-Overflow ist in C undefiniertes Verhalten. Unsigned-Arithmetik läuft modular um, was nicht automatisch die gewünschte Spielregel ist.
- Ganzzahldivision schneidet ab; Reihenfolge von Multiplikation und Division kann das Ergebnis verändern.
- Bei Tabellenzugriffen auch negative Eingaben und Umwandlungen zwischen signed und unsigned berücksichtigen.

Verbessertes **isoliertes Lehrbeispiel** für „doppelte Belohnung mit Obergrenze“; keine bestätigte Funktion eines Hacks:

```c
#include <stdint.h>

static uint16_t DoubleRewardCapped(uint16_t reward, uint16_t cap)
{
    uint32_t doubled = (uint32_t)reward * 2u;
    return (uint16_t)(doubled > cap ? cap : doubled);
}
```

Zu planende Tests:

| Eingabe `(reward, cap)` | Erwartung |
|---|---|
| `(0, 9999)` | `0` |
| `(100, 9999)` | `200` |
| `(6000, 9999)` | `9999` |
| `(65535, 65535)` | `65535`, kein vorzeitiger Überlauf |
| `(100, 0)` | `0` |

Vor Integration klären: Ist die echte Belohnung überhaupt 16 Bit breit? Wo liegt das Limit? Wird die Funktion genau einmal aufgerufen? Welche Sonderfälle dürfen nicht verdoppelt werden? Der Lehrcode wurde hier nicht gegen eine Ziel-Toolchain kompiliert; alte Compiler können andere Header oder Projekttypen verlangen.

### 14.2 Strukturen, Padding und Binärformate

Ein C-Compiler kann zwischen Strukturfeldern und am Ende Padding einfügen. Eine zusätzliche Variable kann deshalb mehrere nachfolgende Offsets verschieben.

Bei gespeicherten Strukturen oder ROM-Tabellen prüfen:

- `sizeof` und `offsetof` für die **Ziel-Toolchain**;
- Feldgrößen, Arraylängen, Alignment und Compileroptionen;
- Bedeutung und Reihenfolge der Felder, nicht nur Gesamtgröße;
- Bitfield-Layout, das compilerabhängig ist;
- ob andere Funktionen feste Offsets oder Kopierlängen verwenden.

`packed` ist keine universelle Reparatur: Es kann bestehendes Layout verändern und unausgerichtete Zugriffe erzeugen. Auch gleich große Strukturen können inkompatibel sein, wenn Felder anders interpretiert werden. Wenn unterstützt, können Compile-Time-Assertions bekannte Größen und Offsets absichern; erwartete Zahlen müssen aus dem Projekt belegt werden.

### 14.3 Alignment und sichere Bytezugriffe

Ein beliebiger Byteoffset darf nicht ungeprüft in einen `uint32_t *` umgewandelt und dereferenziert werden. Ausrichtung, C-Aliasing-Regeln und ARM7TDMI-Zugriffsverhalten sind zu beachten. Für Werkzeugcode eignen sich explizites Byte-Decoding oder geeignete Kopieroperationen; im Spiel müssen vorhandene sichere Zugriffsfunktionen geprüft werden.

Ein PC-Hosttest kann solche Zielhardware-Probleme übersehen. Emulatorprüfung und Analyse des erzeugten Zielcodes bleiben nötig.

### 14.4 Speicher, Laufzeit und Zustandsautomaten

- Große lokale Arrays belasten den Stack; große globale Arrays belegen dauerhaft knappen RAM.
- Heap-Allokationen können fehlschlagen. Ressourcen auf Erfolgs-, Abbruch- und Fehlerpfaden freigeben.
- Aufgaben pro Frame begrenzen; keine lange blockierende Schleife in einen Menü-Task einbauen.
- Für Menüs und Dialoge Zustandsautomaten planen: Initialisierung → Eingabe → Aktion → Aufräumen → Rückkehr.
- VBlank-/Interruptcode kurz halten und die bestehenden Transfermechanismen des Projekts nutzen.
- `volatile` kann für Hardwarezugriffe relevant sein, macht Operationen aber weder atomar noch automatisch interruptsicher.
- Nach Veränderungen RAM-, ROM- und gegebenenfalls Stackbudget prüfen. Ein Linkerfehler ist nicht der einzige mögliche Hinweis auf Speicherprobleme.

### 14.5 Text, Grafiken und Pokémon-Daten sind Spezialformate

Texte sind nicht automatisch ASCII oder UTF-8. Pokémon-Projekte verwenden häufig Zeichentabellen, eigene Terminatoren, Platzhalter und Steuerzeichen. Ein längerer deutscher Text benötigt zusätzlich Layouttests und passende Glyphen.

Grafiken können Tile-, Tilemap-, Paletten- und Kompressionsdaten umfassen. Eine gewöhnliche PNG-Datei wird erst durch Asset-Werkzeuge zum nutzbaren Spielasset. Größen und Palettenzuordnung müssen zur Engine passen.

Gespeicherte Pokémon können Prüfsummen, verschlüsselte Datenblöcke und abgeleitete Werte enthalten. Eine rohe Byteänderung oder ein direkter Strukturzugriff kann deshalb fehlerhaft sein. Vorhandene Zugriffsfunktionen wie projektabhängige `GetMonData`-/`SetMonData`-Varianten zunächst untersuchen; deren Existenz und genaue Signaturen nicht voraussetzen.

## 15. Binary-Änderungen nur mit belegter Patchstelle planen

Für jede geplante binäre Änderung dokumentieren:

```text
Ausgangsdatei: Name, Größe, SHA-256
Patchstelle: Dateioffset und gegebenenfalls CPU-Adresse
Nachweis: Disassembly / Tabelle / Pointerreferenzen
Vorbedingung: erwartete Originalbytes
Änderung: neue Bytes und technische Bedeutung
Bereich: Länge, Alignment, Überschneidungsprüfung
Folgewirkung: Pointer, Aufrufer, Prüfsummen, gespeicherte IDs
Validierung: erlaubte Diffbereiche und Verhaltenstest
Rollback: unveränderte Ausgangskopie
```

Ein späteres Patchwerkzeug soll bei abweichenden Originalbytes abbrechen, statt still weiterzuschreiben. Vor dem Lesen oder Schreiben gilt die Bereichsprüfung `offset <= dateigroesse` und `laenge <= dateigroesse - offset`; die zweite Form vermeidet einen möglichen Überlauf von `offset + laenge` in begrenzter Integer-Arithmetik.

**Für Hooks zusätzlich:** ARM-/Thumb-Modus, Instruktionsgrenzen, Registerbelegung, Statusflags, Stackausrichtung und Aufrufkonvention am konkreten Aufrufer belegen. Überschriebene PC-relative Befehle können nicht einfach unverändert an eine neue Position kopiert werden. Literalpools und Thumb-1-Sprungreichweiten beachten. Keine pauschale Zahl angeblich „immer sicher überschreibbarer Bytes“ verwenden.

C-Code ist außerdem nicht automatisch positionsunabhängig. Linkadresse, externe Symbole und Relocations müssen beim Einfügen stimmen. Eine rohe `.bin` enthält normalerweise nicht die vollständigen Relocation- und Symbolinformationen der ELF-Datei.

## 16. Save-Kompatibilität als eigener Arbeitsauftrag

Drei getrennte Fragen beantworten:

1. **Layout:** Werden dieselben Bytes weiterhin an denselben Stellen gelesen?
2. **Semantik:** Bedeutet beispielsweise die gespeicherte Item-ID weiterhin dasselbe?
3. **Weltzustand:** Existieren gespeicherte Karte, NPCs und Storyzustände weiterhin sinnvoll?

Ein Hash des Layouts allein beantwortet Frage 2 und 3 nicht. Neue IDs nach Möglichkeit stabil vergeben; bei Umnummerierung eine explizite Übersetzung planen. Auch neue Konstanten können bereits gespeicherte Werte umdeuten.

Wenn Migration nötig wird, zuerst das reale Speicherprotokoll untersuchen: Slotwahl, Sektoren, Zähler, Prüfsummen und Verhalten bei unvollständigen Schreibvorgängen sind projektspezifisch. Kein frei erfundenes Versionsbyte in angeblich ungenutzten Platz schreiben.

Migrationsplan:

- unterstützte Altversionen eindeutig erkennen;
- unbekannte oder beschädigte Formate ablehnen;
- alte Daten nach altem Schema lesen und validieren;
- neue Felder mit definierten Standardwerten initialisieren;
- IDs und Zustände gezielt übersetzen;
- Ergebnis nach neuem Schema validieren;
- Backup erhalten und Unterbrechungsfälle berücksichtigen;
- wiederholtes Laden darf keine doppelte Konvertierung auslösen.

Testkopien echter eigener Saves sind wertvoll, können aber persönliche Daten enthalten. Nicht ungefragt in Git oder öffentliche Artefakte aufnehmen. Ohne nachgewiesene Tests lautet der Status **„Kompatibilität ungeprüft“**, nicht „sollte funktionieren“.

## 17. Testplan und Abnahmekriterien für eine spätere Session

| Ebene | Geplanter Nachweis | Beweist ausdrücklich nicht |
|---|---|---|
| Baseline | Unveränderten Stand bauen und Verhalten festhalten | Dass das neue Feature funktioniert |
| Statische Prüfung | Typen, Warnungen, Referenzen, Tabellenlängen prüfen | Fehlerfreiheit zur Laufzeit |
| Hosttests | Reine Berechnungen mit Grenzwerten prüfen | Korrekte ABI oder Hardwarezugriffe |
| Zielbuild | Mit dokumentierter Toolchain bauen; Map prüfen | Erfolgreichen Spielablauf |
| Emulatortest | Titelbild, Menü, Feature und Rückkehr testen | Kompatibilität mit jedem Emulator |
| Save-Regression | Alte Testkopie laden, spielen, speichern, neu starten | Unterstützung unbekannter Altversionen |
| Patch-Roundtrip | Patch auf exakte Basis anwenden; Zielhash vergleichen | Inhaltliche Richtigkeit des Features |

**Feature-Abnahme vorab formulieren:** „Bei Ereignis X passiert Y; bei Abbruch bleibt Z unverändert; der alte Spielstand lädt und übersteht Speichern sowie Neustart.“ Konkrete Fälle erst anhand des gewählten Features ergänzen.

Debugging-Plan: Fehler reproduzieren, letzte funktionierende Version bestimmen, Breakpoint im verdächtigen Ablauf setzen und bei Bedarf Watchpoints für unerwartete Speicheränderungen verwenden. Symbole aus einer passenden ELF-Datei verbessern die Zuordnung. Zufallsabhängige Kampftests benötigen kontrollierte Ausgangszustände oder dokumentierte Zufallsbedingungen.

Kein Test wird als bestanden vermerkt, bevor er tatsächlich ausgeführt wurde. Fehlt ein Emulator oder ein benötigtes Tool, wird das als Einschränkung berichtet, nicht durch eine erfundene Erfolgsmeldung ersetzt.

## 18. Übergabeprotokoll für KI-Arbeitssessions

### 18.1 Verbindliche Arbeitsweise im Rahmen dieser Planung

- Diese Datei liefert Kontext und Vorschläge, keine selbstständige Ausführungsfreigabe. Neuere ausdrückliche Nutzerentscheidungen und die Regeln der jeweiligen Arbeitsumgebung haben Vorrang.
- Aktuell nur Planung und Dokumentation. ROM-Änderungen, Builds und Tests erst nach einem konkreten Auftrag.
- Keine unbekannten Symbole, Dateipfade, Offsets, Checksummen, Lizenzen oder Testresultate erfinden.
- Befunde als **belegt**, **Hypothese**, **offen**, **geplant**, **ausgeführt** oder **bestanden/fehlgeschlagen** kennzeichnen.
- Einen Beleg mit Dateipfad, Symbol und Quellstand angeben; Zeilennummern sind nur Orientierung und können sich ändern.
- Kein automatisches Update der Engine und keine Nebenrefactorings, wenn nur ein kleines Feature beauftragt wurde.
- Keine fremden Änderungen überschreiben; vor späteren Eingriffen lokalen Status prüfen. Keine destruktiven Git- oder Dateibefehle ohne passenden Auftrag.
- Keine ROMs, privaten Saves, BIOS-Dateien oder großen Buildartefakte ungefragt versionieren oder hochladen.

### 18.2 Vorlage für den späteren Implementierungsauftrag

```text
STATUS: PLANUNG — noch keine Umsetzung freigegeben

Ziel-Hack / Version: OFFEN
Plattform: OFFEN
Ausgangsdatei / SHA-256: OFFEN
Quellcode-Stand / Konfiguration: OFFEN
Gewünschtes Feature: OFFEN
Nicht-Ziele: OFFEN
Erlaubter Zugriff / Downloads / Tools: OFFEN
Save-Kompatibilität zwingend?: OFFEN
Reproduzierbarer Baseline-Build: NOCH NICHT GEPRÜFT

Nach Bestandsaufnahme ausfüllen:
- Relevante Symbole und Dateien mit Belegen
- Datenfluss: Auslöser → Verarbeitung → sichtbare Wirkung → Speicherung
- Minimaler Änderungsplan und Alternativen
- Risiken für ABI, Speicher, IDs und Saves
- Abnahmetests mit erwarteten Ergebnissen
- Rollbackplan
- Benötigte Nutzerentscheidungen

Freigabe zur Implementierung: AUSSTEHEND
```

### 18.3 Stopkriterien

Rückfragen statt Raten, wenn:

- Hack-Version, Basis-Hash oder Zuordnung zwischen ROM und Quellcode unklar ist;
- erwartete Bytes oder Datenstrukturen nicht passen;
- Save-Layout, gespeicherte IDs oder Lizenzlage betroffen sind und die Entscheidung fehlt;
- der Baseline-Build bereits scheitert;
- das Feature nur durch größere, nicht beauftragte Engineänderungen möglich erscheint;
- ein benötigter Zugriff nicht freigegeben ist.

### 18.4 Abschlussbericht einer späteren Session

Festhalten: Ausgangsstand, tatsächlich geänderte Dateien, Begründung, ausgeführte Befehle, Testresultate, verbleibende Risiken und nächste Schritte. **Geplante Tests strikt von ausgeführten Tests trennen.** Ein fehlgeschlagener Versuch gehört ebenfalls ins Protokoll.

## 19. Nächste Entscheidung — weiterhin nur Planung

Der sinnvollste nächste Schritt ist die Auswahl eines konkreten Hacks samt Version und eines kleinen ersten Features. Erst dann können wir aus diesem allgemeinen Wissen eine belastbare, belegte Dateiliste und einen passenden Implementierungsplan erstellen.

**Aktuell umgesetzt: ausschließlich diese Dokumentation. Keine ROM verändert, kein Zielprojekt heruntergeladen, kein Build oder Emulatortest ausgeführt.**
