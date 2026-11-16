"""Gemeinsames Startmaterial: Beispieldaten, Parameterschema und Zeitprüfung."""
from datetime import date as Date
from typing import Annotated, Literal

from fastmcp.exceptions import ToolError
from pydantic import Field

Room = Annotated[Literal["A", "B", "C"], Field(description="Kennung des Lernraums")]
Day = Annotated[Date, Field(description="Kalendertag am Campus, JJJJ-MM-TT")]
Clock = Annotated[str, Field(pattern=r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$", description="Ortszeit in HH:MM")]
People = Annotated[int, Field(gt=0, strict=True, description="Anzahl der Personen")]
CAPACITY = {"A": 6, "B": 4, "C": 8}
DEMO_DAY = Date(2026, 11, 20)


def initial_plan():
    # Schlüssel: (Raum, Datum); Werte: belegte Intervalle [Beginn, Ende).
    return {("A", DEMO_DAY): [("16:00", "17:00")],
            ("C", DEMO_DAY): [("15:00", "16:00")]}


def minutes(clock: str) -> int:
    hour, minute = map(int, clock.split(":"))
    return 60 * hour + minute


def duration(start: str, end: str) -> int:
    length = minutes(end) - minutes(start)
    if length <= 0:
        raise ToolError("Das Ende muss am selben Tag nach dem Beginn liegen.")
    return length
