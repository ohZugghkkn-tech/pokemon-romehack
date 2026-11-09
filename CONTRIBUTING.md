# Änderungen an diesem Projekt

## Grenzen und Zuständigkeiten

- **Spiel:** `soulgold/`; Struktur und Codingstil der vorhandenen Engine erhalten.
- **Anzeigeeffekte:** `shaders/`; gehören nicht in die ROM und brauchen keine mitgelieferte Emulator-Konfiguration.
- **Prüfwerkzeuge:** `scripts/` mit eigenen Regressionstests.
- **Projektregeln:** Root-Dokumentation und `.github/`; die verschachtelte Upstream-`.github/` ist hier nicht aktiv.

Keine unnötigen Umbenennungen oder Massenformatierung des vendorten Codes. Nutzerwunsch und Beleg vor Featureänderung. Bei Save-, ID- oder Datenlayoutänderungen zusätzlich Migration und Altstandtests planen. Mew als Starter ist noch kein abgeschlossener Bestandteil.

## Vor einer Änderung

1. Herkunft und Einschränkungen in `UPSTREAM.json` und `docs/upstream-changes.md` lesen.
2. Arbeitsstand prüfen; vorhandene fremde Änderungen nicht überschreiben.
3. Problem reproduzieren und tatsächliche Eingabequelle identifizieren (nicht generierten Header bearbeiten).
4. Prüferwartung aus gewünschtem Verhalten oder Codevertrag ableiten. Tests nicht nur so ändern, dass eine Regression grün wird.
5. Neue Prüfwerkzeuge selbst mit positiven und negativen Fällen testen.

## Prüfung und Review

- `make check` nach `TESTING.md` ausführen; dies ist nur der Host-Testumfang.
- Spieländerungen zusätzlich mit `make rom`, `make target-tests` und im Spiel prüfen.
- Shaderänderungen zusätzlich kompilieren und visuell vergleichen; Screenshots ohne verteilte ROM beilegen.
- Bekannte Layoutabweichungen nicht blind mit Nullen auffüllen, abschneiden oder umdimensionieren. Ihre Herkunft, Erreichbarkeit und beabsichtigten Dimensionen zuerst klären.
- Neue Abweichungen in `docs/known-layout-issues.json` nicht einfach zulassen, um einen roten Test zu umgehen. Eine Baseline ist eine Debt-Liste, keine Fehlerbehebung.
- Kommandos, Umgebung, fehlgeschlagene Tests und nicht ausgeführte Prüfungen angeben. Keine Prozentangabe zur Testabdeckung aus Testanzahl ableiten.
- KI-Unterstützung offenlegen; Menschen müssen relevante Änderungen und Freigaben prüfen. Externe Projekte können eigene strengere Regeln haben, die bei Beiträgen dorthin gelten.

## Sicherheit und Rechte

Keine Secrets, ROMs, BIOS-Dateien, echten Saves oder lokale Umgebungen committen. Originale Copyright-/Lizenzhinweise erhalten; keine pauschale Lizenz des ganzen Repositories erfinden. Fehlerberichte mit Version, reproduzierbaren Schritten und erwarteten Ergebnissen reichen normalerweise ohne vollständige Spieldateien aus.

Ein PR darf Builds prüfen, aber keine ungeprüften Veröffentlichungen anlegen. Merge und Release sind separate Entscheidungen. Freigabeanforderungen stehen in `docs/RELEASE-CHECKLIST.md`.
