# Live-Demonstration: Sprechtext für Fatma und Nikolas

**Einstieg**

„Wir haben bisher gesehen, wie ein Sprachmodell Werkzeuge anfordern kann. Jetzt bauen und testen wir selbst einen kleinen MCP-Server. Unser Beispiel ist ein Campusshop mit vier Produkten. Der Server bietet genau zwei Werkzeuge an: `list_products` zum Lesen des Bestands und `buy_product` für einen simulierten Kauf.“

**Start und Werkzeugliste zeigen**

„Ich starte den Python-Server. Über Streamable HTTP ist er lokal unter `http://localhost:8420/mcp` erreichbar. Im Inspector verbinden wir uns und klicken auf ,Tools‘. Das ist wichtig: Hier entscheidet noch kein LLM – wir wählen die Tools selbst aus.“

**Test 1: Lesen**

„Mit `list_products` fragen wir ab, welche Produkte vorhanden sind. Beim Buch *Python Crash Course* sehen wir fünf Exemplare.“

**Test 2: Erfolgreicher Kauf**

„Jetzt wählen wir `buy_product` und übergeben den Produktnamen sowie `quantity = 2`. Der Server prüft die Eingaben, reduziert den Bestand und antwortet: Zwei Exemplare gekauft, Gesamtpreis 49,80 Euro, Restbestand drei.“

**Test 3: Fehlender Bestand**

„Wir versuchen anschließend vier weitere Exemplare zu kaufen. Es sind aber nur noch drei vorhanden. Der Server lehnt den Kauf ab. Wenn wir `list_products` erneut ausführen, sehen wir: Der Bestand ist immer noch drei. Eine fehlgeschlagene Geschäftsaktion darf den Zustand nicht verändern.“

**Rollenspiel als Übertragung auf Reasoning und ReAct**

„Ein Kunde sagt: ,Ich brauche drei Hefte, aber kauf erst nach meinem Ja.‘ Unser Bestand ist zwei. Deshalb fragt die Person in der Assistentenrolle zunächst mit `list_products` nach und antwortet: ,Wir haben nur zwei. Möchtest du beide?‘ Noch führen wir `buy_product` nicht aus. Erst nach der Antwort ,Ja, zwei‘ führen wir den simulierten Kauf aus. Das Ergebnis der Abfrage hat die nächste Entscheidung verändert – genau der Gedanke hinter ReAct. Ein Modell ist in dieser Rollenspielvariante noch nicht angebunden.“

**Abschlussfrage**

„Woran erkennt man, dass etwas wirklich passiert ist? Nicht daran, dass der Assistent ,gekauft‘ sagt, sondern an der tatsächlichen Rückmeldung des Servers und dem veränderten Bestand. Und wer hat im Inspector die Funktion ausgewählt? Wir selbst. Bei einer angebundenen LLM-Anwendung könnte diese Werkzeuganforderung vom Modell stammen.“
