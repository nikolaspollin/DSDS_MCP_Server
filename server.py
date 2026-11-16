"""Musterlösung: ein lokaler MCP-Server für einen fiktiven Hochschulcampus."""
import argparse
from uuid import uuid4

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from raumplan import CAPACITY, Clock, Day, People, Room, duration, initial_plan


def create_server(*, booking_allowed: bool = True) -> FastMCP:
    mcp = FastMCP("Lernräume am Campus")
    plan = initial_plan()

    def first_conflict(room, date, start, end):
        for other_start, other_end in sorted(plan.get((room, date), [])):
            if start < other_end and other_start < end:
                # Nur den Teil melden, der im angefragten Zeitraum liegt.
                return {"start_time": max(start, other_start), "end_time": min(end, other_end)}
        return None

    @mcp.tool(annotations={"readOnlyHint": True})
    async def check_room_availability(room: Room, date: Day, start_time: Clock, end_time: Clock) -> dict:
        """Prüft das gesamte Zeitfenster. Liefert Plätze und ggf. die erste Überschneidung."""
        duration(start_time, end_time)
        conflict = first_conflict(room, date, start_time, end_time)
        return {"room": room, "capacity": CAPACITY[room], "available": conflict is None,
                "conflict": conflict}

    @mcp.tool
    async def book_room(room: Room, date: Day, start_time: Clock, end_time: Clock, people: People) -> dict:
        """Reserviert nach ausdrücklicher Freigabe im Host. Nur bei Erfolg eine Buchung zusagen."""
        if not booking_allowed:
            raise ToolError("Lesemodus: keine Berechtigung zum Buchen.")
        if duration(start_time, end_time) > 120:
            raise ToolError("Je Reservierung sind höchstens zwei Stunden erlaubt.")
        if people > CAPACITY[room]:
            raise ToolError(f"Raum {room} hat nur {CAPACITY[room]} Plätze.")
        # Kein await zwischen Prüfung und Eintrag: im einzelnen Serverprozess
        # kann hier kein zweiter MCP-Aufruf dieselbe Lücke buchen.
        if first_conflict(room, date, start_time, end_time):
            raise ToolError(f"Raum {room} ist im gewünschten Zeitraum bereits belegt.")
        plan.setdefault((room, date), []).append((start_time, end_time))
        return {"booking_id": uuid4().hex, "room": room, "date": date.isoformat(),
                "start_time": start_time, "end_time": end_time, "people": people}

    @mcp.resource("campus://booking/rules", mime_type="text/plain")
    def booking_rules() -> str:
        """Buchungsordnung der Lernräume."""
        return ("Je Reservierung sind höchstens zwei Stunden erlaubt. Die Gruppe muss "
                "in den Raum passen. Vor einer verbindlichen Buchung fragt der Host nach.")

    @mcp.prompt
    def lernraum_anfragen(anfrage: str) -> str:
        """Gesprächseinstieg für die Lernraumsuche."""
        return (f"Anliegen der Gruppe: {anfrage}\n"
                "Übernimm bekannte Angaben. Frage nur nach fehlendem Datum, Zeitfenster "
                "oder Gruppengröße. Prüfe die gewünschten Räume und nenne den Konflikt "
                "oder die passende Alternative. Warte auf ein ausdrückliches Ja vor der Buchung.")

    return mcp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--read-only", action="store_true", help="Buchungsrecht für diese Demo entziehen")
    args = parser.parse_args()
    create_server(booking_allowed=not args.read_only).run(
        transport="streamable-http", host="127.0.0.1", port=8420)
