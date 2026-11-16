"""Arbeitsdatei: aus dem Projektordner mit uv run -m starter.server starten."""
from uuid import uuid4

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from raumplan import CAPACITY, Clock, Day, People, Room, duration, initial_plan

mcp = FastMCP("Lernräume – Werkstatt")
plan = initial_plan()


def first_conflict(room, date, start, end):
    # TODO 1: Belegungen von (room, date) prüfen; erste Überschneidung
    # als {"start_time": ..., "end_time": ...} liefern, sonst None.
    raise NotImplementedError


@mcp.tool(annotations={"readOnlyHint": True})
async def check_room_availability(room: Room, date: Day, start_time: Clock, end_time: Clock) -> dict:
    """Prüft den Raum für das gesamte Zeitfenster, ohne ihn zu reservieren."""
    # TODO 2: Reihenfolge der Zeiten prüfen, Kapazität und Konflikt zurückgeben.
    raise ToolError("Die Raumprüfung fehlt noch.")


# TODO 3: book_room als zweites Tool registrieren. Benötigt zusätzlich people: People.
# TODO 4: Buchungsordnung als Resource und Gesprächseinstieg als Prompt anbieten.


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8420)
