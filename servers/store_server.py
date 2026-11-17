"""Lehrbeispiel für Pamela Fox, Exercise 3: eigener MCP-Campusshop.

Start: uv run servers/store_server.py
MCP-Endpunkt: http://localhost:8420/mcp
"""

import logging
from typing import Annotated

from fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("CampusShopMCP")
logger.setLevel(logging.INFO)

mcp = FastMCP("Campusshop")

# Diese Daten liegen nur im Arbeitsspeicher. Bei einem Neustart wird
# der ursprüngliche Bestand wiederhergestellt.
INVENTORY: dict[str, dict[str, float | int]] = {
    "Heft": {"price": 2.50, "quantity": 2},
    "Python Crash Course": {"price": 24.90, "quantity": 5},
    "Collegeblock": {"price": 4.20, "quantity": 8},
    "Kugelschreiber": {"price": 1.80, "quantity": 12},
}


def get_inventory() -> dict[str, dict[str, float | int]]:
    """Liefere eine Kopie des Inventars (für Tool und Logiktests)."""
    return {name: details.copy() for name, details in INVENTORY.items()}


def purchase(product_name: str, quantity: int) -> str:
    """Führe ausschließlich die Geschäftslogik für den simulierten Kauf aus."""
    if product_name not in INVENTORY:
        return f"Kauf abgelehnt: Produkt '{product_name}' existiert nicht."

    if quantity <= 0:
        return "Kauf abgelehnt: Die Menge muss größer als null sein."

    item = INVENTORY[product_name]
    remaining = int(item["quantity"])
    if quantity > remaining:
        return (
            f"Kauf abgelehnt: Für '{product_name}' sind nur "
            f"{remaining} Exemplare verfügbar; angefragt wurden {quantity}."
        )

    item["quantity"] = remaining - quantity
    total = float(item["price"]) * quantity
    return (
        f"Simulierter Kauf erfolgreich: {quantity} x {product_name}. "
        f"Gesamtpreis: {total:.2f} EUR. "
        f"Verbleibender Bestand: {item['quantity']}."
    )


@mcp.tool
async def list_products() -> dict[str, dict[str, float | int]]:
    """Zeige alle verfügbaren Produkte mit Preisen und aktuellem Lagerbestand."""
    return get_inventory()


@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Exakter Produktname aus list_products"],
    quantity: Annotated[int, "Anzahl der zu kaufenden Exemplare; muss positiv sein"],
) -> str:
    """Simuliere einen Kauf. Nur gültige Käufe reduzieren den Lagerbestand."""
    return purchase(product_name, quantity)


if __name__ == "__main__":
    logger.info("Campusshop MCP server starting (HTTP mode on port 8420)")
    # Wie im Tutorial: Streamable HTTP. Nur in einer vertrauenswürdigen
    # lokalen Demo-Umgebung verwenden; nicht ungeschützt ins Netz stellen.
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8420)
