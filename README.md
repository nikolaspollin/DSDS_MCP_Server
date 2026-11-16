# Lernräume buchen mit MCP

**Seminar Sprachdialogsysteme · Musterlösung und praktische Übung (75 Minuten)**

„Wir sind zu viert und brauchen am 20. November 2026 ab 15 Uhr für zwei Stunden einen Lernraum. Prüfe zuerst A, dann bei Bedarf B. Buche erst, wenn wir bestätigen.“

Der Host leitet die Endzeit 17 Uhr aus dem Auftrag ab. Ob der Raum tatsächlich frei ist, kann nur der Server beantworten. Nach dem Konflikt in A prüft der Host B und wartet auf das Ja der Gruppe. Genau dieser Wechsel zwischen Gespräch, Tool-Aufruf und Rückmeldung ist der Kern der Übung.

**Für Teilnehmende:** [Arbeitsblatt](UEBUNG.md) und [Starter](starter/server.py). **Für die Seminarleitung:** [fertiger Server](server.py), [ausführbarer Vortragsdialog](demo_client.py) und die folgenden Demo-Schritte.

## Die Musterlösung vorführen

Alle Befehle im Projektordner ausführen. Voraussetzung: [uv](https://docs.astral.sh/uv/getting-started/installation/); empfohlen ist Python 3.12. Der erste Start lädt Abhängigkeiten, dafür Internet einplanen. Für die Terminaldemo sind weder API-Schlüssel noch Modellzugang nötig.

**Terminal 1** – Umgebung vorbereiten und Server starten:

```sh
uv sync --locked --python 3.12
uv run server.py
```

**Terminal 2** – mit dem laufenden Server sprechen:

```sh
uv run demo_client.py
```

1. Beim ersten Durchgang mit **nein** antworten. A meldet den Konflikt 16–17 Uhr; B ist frei. Die Ablehnung lässt B unverändert.
2. Client erneut starten, diesmal mit **ja** bestätigen. Der Host ruft erst jetzt `book_room` auf und liest die Buchungs-ID aus dem Ergebnis.
3. Client ein drittes Mal starten. Jetzt sind A und B belegt. Vor einer weiteren Vorführung den **Server** mit Strg+C beenden und neu starten.

Der Terminalclient ist ein kleines, fest programmiertes Beispiel für den Host. Er zeigt die Freigabe reproduzierbar. Wer dieselbe Aufgabe mit einem Sprachmodell ausprobieren möchte, öffnet diesen Projektordner in VS Code: Die [MCP-Konfiguration](.vscode/mcp.json) verweist auf den laufenden Server. In einem MCP-fähigen Chat den Auftrag oben eingeben, die tatsächlichen Aufrufe kontrollieren und erst in einem zweiten Gesprächsschritt die Buchung bestätigen.

## Was der Server bereitstellt

| Schnittstelle | Was ihr daran zeigen könnt |
| --- | --- |
| Tool `check_room_availability(room, date, start_time, end_time)` | Liest Kapazität und Belegung. Ein Konflikt ist eine erfolgreiche Auskunft mit `available: false`; `conflict` zeigt die erste zeitliche Überschneidung. |
| Tool `book_room(room, date, start_time, end_time, people)` | Prüft Schreibrecht, Dauer, Gruppengröße und aktuelle Belegung. Nur ein erfolgreicher Eintrag liefert eine Buchungs-ID. |
| Resource `campus://booking/rules` | Macht die Buchungsordnung lesbar, u. a. die Obergrenze von zwei Stunden pro Reservierung. |
| Prompt `lernraum_anfragen(anfrage)` | Liefert eine Vorlage für Rückfragen: bekannte Angaben übernehmen, fehlende erfragen und vor der Reservierung die Gruppe entscheiden lassen. |

**Beispielplan am 20.11.2026** (fiktive Daten aus dem Vortrag):

| Raum | Plätze | 15–16 Uhr | 16–17 Uhr |
| --- | ---: | --- | --- |
| A | 6 | frei | belegt |
| B | 4 | frei | frei |
| C | 8 | belegt | frei |

Der Plan enthält anfangs nur die beiden belegten Intervalle aus der Tabelle. Alle weiteren Zeiten sind in dieser Demo frei. Reservierungen gelten nur im laufenden Prozess. Alle verbundenen Clients sehen denselben Plan. Der Server läuft lokal unter `http://127.0.0.1:8420/mcp` (Streamable HTTP).