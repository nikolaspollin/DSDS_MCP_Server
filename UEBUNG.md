# Werkstatt: Kann der Assistent Raum B zusagen?

**75 Minuten · Ziel:** Am Ende kann ein MCP-Client einen belegten Raum erklären, eine passende Alternative prüfen und sie nach Bestätigung tatsächlich buchen. Eine Person programmiert, die andere prüft die Ergebnisse im Inspector. Wechselt nach der Raumprüfung.

**Vor dem Seminar:** Python/uv gemäß README vorbereiten. Für den [MCP Inspector](https://github.com/modelcontextprotocol/inspector) Node.js und npm gemäß dessen Voraussetzungen installieren und `npx @modelcontextprotocol/inspector` einmal starten, damit der Download nicht in die Übungszeit fällt. Ein Modellzugang ist optional.

| Minuten | Arbeitsschritt | Woran ihr erkennt, dass er fertig ist |
| --- | --- | --- |
| 0–8 | Server starten und entdecken | Der Inspector zeigt das Schema der Raumprüfung. |
| 8–18 | Vortragsdaten modellieren | Ihr könnt den Unterschied zwischen Kapazität und zeitlicher Verfügbarkeit am Plan erklären. |
| 18–35 | Belegung prüfen | A meldet die konkrete Überschneidung, B ist frei. |
| 35–53 | Buchung implementieren | Eine Buchung verändert die nächste Abfrage; eine Doppelbuchung scheitert. |
| 53–63 | Resource und Prompt ergänzen | Der Client kann die Regel lesen und die Vorlage abrufen. |
| 63–75 | Vortragsdialog und Gegenproben | Ohne Ja bleibt B frei. Mit Ja entsteht genau eine Buchung. |

### 1 · Verbindung herstellen (8 Minuten)

Arbeitet in `starter/server.py`, die fertige Lösung steht separat in `server.py`. Aus dem Projektordner:

```sh
uv sync --locked --python 3.12
uv run -m starter.server
```

In einem zweiten Terminal `npx @modelcontextprotocol/inspector` starten. Die vom Inspector ausgegebene Browseradresse öffnen, **Streamable HTTP** wählen, als Server-URL `http://127.0.0.1:8420/mcp` eintragen und verbinden. Unter **Tools → List Tools** die vier Pflichtfelder von `check_room_availability` suchen. Welche Werte erlaubt das Feld `room`? Ruft das Tool einmal auf: Die Meldung „Die Raumprüfung fehlt noch“ zeigt, dass der Weg bis zum Handler funktioniert.

Nach jeder Codeänderung den Python-Server mit Strg+C beenden, erneut starten und den Inspector neu verbinden. Einen Starter und eine Musterlösung könnt ihr nicht gleichzeitig auf Port 8420 starten.

### 2 · Den Plan lesen (10 Minuten)

Öffnet `raumplan.py`. Skizziert für A, B und C die beiden Stunden von 15 bis 17 Uhr am 20.11.2026. Was enthält `plan.get(("B", DEMO_DAY), [])`? Weshalb bedeutet eine leere Liste „frei“? Tauscht euch darüber aus, was passiert, wenn jemand für einen anderen Tag fragt.

Ergänzt zum Ausprobieren eine Belegung von B an einem **anderen** Datum. Notiert je ein erwartetes Ergebnis für B am Seminartag und am neuen Datum; prüft beides im nächsten Schritt. Stellt anschließend den Ausgangsplan wieder her.

### 3 · Den Konflikt erklären (17 Minuten)

Implementiert `first_conflict` und `check_room_availability`. `duration` prüft bereits, ob das Ende nach dem Beginn liegt. Die Werte von `Clock` haben immer die Form HH:MM, deshalb lassen sie sich direkt vergleichen. Beachtet die Grenze: Eine Anfrage bis 16:00 verträgt sich mit einer Belegung ab 16:00. Wenn sich Intervalle schneiden, gebt nur ihren gemeinsamen Teil zurück.

Inspector-Aufruf für die Folie:

```json
{"room":"A","date":"2026-11-20","start_time":"15:00","end_time":"17:00"}
```

Soll-Ergebnis: `{"room":"A","capacity":6,"available":false,"conflict":{"start_time":"16:00","end_time":"17:00"}}`. Für B erwartet ihr vier Plätze, `available: true` und `conflict: null`. Testet A bis **16:00** und mit vertauschten Uhrzeiten. Welche Anfrage liefert eine normale Antwort, welche einen Tool-Fehler?

### 4 · Verbindlich buchen (18 Minuten)

Registriert `book_room` als zweites Tool. Es nimmt dieselben vier Argumente an, zusätzlich `people: People`. Erklärt im Docstring, dass der Host die Freigabe einholen muss. Baut die Regeln ein:

1. Eingaben mit `duration` prüfen; bei mehr als 120 Minuten oder zu wenigen Plätzen mit `ToolError` abbrechen.
2. Unmittelbar vor dem Eintrag `first_conflict` prüfen. Ein fremder Client könnte seit der Auskunft bereits gebucht haben. Prüfung und Eintrag im asynchronen Handler direkt nacheinander ohne `await` ausführen.
3. Das belegte Intervall in den Plan eintragen. Als Quittung Raum, Datum, Zeiten, Personenzahl und eine neue `booking_id` (z. B. `uuid4().hex`) zurückgeben.

Bucht B im Inspector für vier Personen von 15 bis 17 Uhr. Bei einem zweiten identischen Aufruf muss ein Tool-Fehler entstehen. Startet den Server danach neu. Was muss passieren, wenn zuerst **fünf** Personen buchen möchten und anschließend vier?

### 5 · Regel und Gesprächsvorlage anbieten (10 Minuten)

Registriert mit `@mcp.resource("campus://booking/rules", mime_type="text/plain")` eine Funktion ohne Argumente, die die Buchungsordnung als Text liefert. Ergänzt mit `@mcp.prompt` eine Funktion `lernraum_anfragen(anfrage: str) -> str`. Baut die Anfrage, den Umgang mit fehlenden Angaben und die Rückfrage vor der Buchung in die Vorlage ein.

Lest die Resource im Inspector unter **Resources** und ruft die Vorlage unter **Prompts** mit „Wir brauchen morgen einen Raum für vier“ ab. Welche Angabe fehlt? Prüft danach B: Das Lesen und der Vorlagenabruf dürfen keine Reservierung ausgelöst haben.

### 6 · Den ganzen Dialog prüfen (12 Minuten)

Startet mit einem frischen Plan. Lasst in einem zweiten Terminal `uv run demo_client.py` gegen **euren** Server laufen. Antwortet erst mit „nein“, im zweiten Durchgang mit „ja“. Prüft B anschließend im Inspector. Falls ihr VS Code mit einem MCP-fähigen Chat nutzt, könnt ihr dieselbe Szene mit dem Auftrag aus der README durchspielen. Vor der Buchungsfreigabe dürfen dort nur lesende Aufrufe zu sehen sein.

Diskutiert anhand eurer Ergebnisse: Welche Information konnte der Host aus „ab 15 Uhr für zwei Stunden“ herleiten? Welche brauchte einen Tool-Aufruf? Was löste den Wechsel von A zu B aus? Ab welchem Ergebnis darf der Assistent „reserviert“ sagen?

**Falls Zeit bleibt:** Zwei Clients prüfen B, solange er frei ist. Client 1 bucht, Client 2 versucht danach zu buchen. Formuliert für Client 2 eine Antwort, die zur tatsächlichen Tool-Rückmeldung passt. Die Musterlösung zeigt mit `--read-only` außerdem, wie der Dienst trotz eines Ja im Dialog eine Buchung mangels Berechtigung ablehnt.
