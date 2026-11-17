"""Logische Tests ohne externe Buchungen oder Zahlungen."""
import unittest

from servers import store_server


class ShopTests(unittest.TestCase):
    def setUp(self):
        store_server.INVENTORY["Heft"]["quantity"] = 2
        store_server.INVENTORY["Python Crash Course"]["quantity"] = 5

    def test_product_list(self):
        products = store_server.get_inventory()
        self.assertIn("Heft", products)
        self.assertEqual(products["Heft"]["quantity"], 2)

    def test_successful_purchase(self):
        result = store_server.purchase("Python Crash Course", 2)
        self.assertIn("erfolgreich", result)
        self.assertEqual(store_server.INVENTORY["Python Crash Course"]["quantity"], 3)

    def test_insufficient_stock(self):
        result = store_server.purchase("Heft", 3)
        self.assertIn("abgelehnt", result)
        self.assertEqual(store_server.INVENTORY["Heft"]["quantity"], 2)

    def test_invalid_quantity(self):
        result = store_server.purchase("Heft", 0)
        self.assertIn("abgelehnt", result)
        self.assertEqual(store_server.INVENTORY["Heft"]["quantity"], 2)

    def test_unknown_product(self):
        result = store_server.purchase("Unbekannt", 1)
        self.assertIn("abgelehnt", result)


if __name__ == "__main__":
    unittest.main()
