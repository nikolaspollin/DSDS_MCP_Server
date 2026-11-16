"""Kleiner Host für den Vortragsdialog; die Tool-Aufrufe laufen über HTTP."""
import asyncio

from fastmcp import Client
from fastmcp.exceptions import ToolError

URL = "http://127.0.0.1:8420/mcp"
TERMIN = {"date": "2026-11-20", "start_time": "15:00", "end_time": "17:00"}


async def dialog(client, ask=input, say=print):
    say("Vier Personen, 20.11.2026, ab 15 Uhr für zwei Stunden. Prüfe A, bei Bedarf B.")
    for room in ("A", "B"):
        args = {"room": room, **TERMIN}
        result = (await client.call_tool("check_room_availability", args)).structured_content
        if not result["available"]:
            conflict = result["conflict"]
            say(f"Raum {room} ist von {conflict['start_time']} bis {conflict['end_time']} belegt.")
            continue
        if result["capacity"] < 4:
            say(f"Raum {room} ist zu klein.")
            continue
        if ask(f"Raum {room} ist frei. Für vier Personen von 15 bis 17 Uhr reservieren? [ja/Nein] ").strip().casefold() != "ja":
            say("Keine Buchung vorgenommen.")
            return
        try:
            receipt = (await client.call_tool("book_room", {**args, "people": 4})).structured_content
        except ToolError as error:
            say(f"Buchung abgelehnt: {error}")
            return
        say(f"Raum {room} ist reserviert. Buchungs-ID: {receipt['booking_id']}")
        return
    say("Für den gesamten Zeitraum passt keiner der angefragten Räume.")


async def main():
    async with Client(URL) as client:
        await dialog(client)


if __name__ == "__main__":
    asyncio.run(main())
