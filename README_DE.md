# MCP-Campusshop – Musterlösung

Basierend auf Pamela Fox, PyCon 2026, Exercise 3: https://github.com/pamelafox/pycon2026-mcp-tutorial/blob/main/exercise3.md

## Voraussetzungen

- Python 3.12 oder neuer
- `uv` (Python-Paketmanager)
- Node.js mit `npx` für den MCP Inspector

## Lokaler Start

1. ZIP entpacken und im Terminal in den Projektordner wechseln.
2. Abhängigkeiten einrichten: `uv sync`
3. Server starten: `uv run servers/store_server.py`
4. Dieses Terminal offen lassen.
5. Zweites Terminal öffnen und den MCP Inspector starten: `npx @modelcontextprotocol/inspector`
6. Die in der Konsole angezeigte Inspector-Adresse im Browser öffnen.
7. Im Inspector **Streamable HTTP** und die Server-URL `http://localhost:8420/mcp` wählen; anschließend verbinden.
8. Im Bereich **Tools** die Werkzeuge anzeigen und Testaufrufe durchführen.

Bei der Verwendung von Windows PowerShell sind die Befehle gleich. Falls `npx` nicht erkannt wird, Node.js installieren und das Terminal erneut öffnen.

## Beispieltests

1. `list_products` zeigt u.a. `Python Crash Course` mit Bestand **5**.
2. `buy_product(product_name="Python Crash Course", quantity=2)` muss den Bestand auf **3** reduzieren; Preis **49,80 EUR**.
3. `buy_product(product_name="Python Crash Course", quantity=4)` wird abgelehnt; Bestand bleibt **3**.
4. Für das Rollenspiel: `Heft` hat anfangs Bestand **2**. Bei Anfrage nach **3** Heften zuerst nur `list_products` ausführen und antworten: „Es gibt nur 2; möchtest du diese beiden kaufen?“ Ohne Zustimmung **nicht** `buy_product` ausführen. Nach „Ja, zwei“ `buy_product(product_name="Heft", quantity=2)` aufrufen. Der Bestand wird **0**.
5. Für einen Neustart mit Ausgangsbestand den Server stoppen (`Ctrl+C`) und erneut starten. Der Bestand wird nur im RAM gehalten.

Optionaler Logiktest: `uv run python -m unittest discover -s tests -v`

## Wichtige fachliche Einordnung

- Der MCP Inspector ist **kein Sprachmodell**. Die Testperson wählt Werkzeuge und Argumente selbst.
- `buy_product` hat **keine eigene Zustimmungs-/Authentifizierungsprüfung**. Die Zustimmung wird im Rollenspiel durch die Person in der Assistentenrolle beachtet; in einem realen Produkt müsste dies die Anwendung bzw. der Dienst technisch absichern.
- Es werden keine echten Bestellungen oder Zahlungen durchgeführt.
- Eine abgelehnte Bestellung ist fachlich fehlgeschlagen, obwohl das Tool technisch ausgeführt werden konnte.
- Diese Musterlösung ist für lokale Demonstrationen, nicht für einen produktiven ungeschützten Server gedacht.

## Optional: Schritt 6 – Coding-Agent in VS Code anbinden

Die Datei `.vscode/mcp.json` ist bereits vorbereitet. Lass den Shop-Server laufen, öffne VS Code im Projektordner und starte den MCP-Server-Eintrag, falls die Oberfläche einen Start-Button anzeigt. Stelle im Copilot-Chat im Agent-Modus sicher, dass die beiden Shop-Tools eingeschaltet sind. Frage dann zum Beispiel: **„Welche Produkte hat der Campusshop?“** Achte darauf, dass der Agent wirklich das MCP-Tool benutzt und nicht lediglich die offen angezeigte Python-Datei ausliest.

Ohne eingerichteten Coding-Agenten funktioniert die Übung mit dem MCP Inspector trotzdem. Hier fordert ein Mensch die Tools an, nicht ein Sprachmodell.

## Optional: Schritt 8 – MCPJam

Die Originalanleitung nutzt außerdem MCPJam. Lokal starten mit `npx @mcpjam/inspector@latest`, dann den HTTP-Server `http://localhost:8420/mcp` hinzufügen und in der Tools- oder Chatansicht testen. Diesen optionalen Schritt bitte nur dann vorführen, wenn er auf eurem Rechner vorher funktioniert hat.

**Teststatus dieser Musterlösung:** Python-Kaufregeln (5 Testfälle) wurden lokal mit einem FastMCP-Ersatzmodul geprüft. Ein echter HTTP-/Inspector-/Coding-Agent-End-to-End-Test war in der Erstellungsumgebung mangels installierbarem FastMCP nicht möglich. Deshalb vor dem Seminar unbedingt auf eurem eigenen Rechner `uv sync`, den Server und den Inspector ausprobieren.
