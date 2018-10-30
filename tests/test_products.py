import unittest
import json

# Local import
from app import create_app
from app.api.v2.database import create_tables, delete_tables


class UserTestCase(unittest.TestCase):

    def setUp(self):
        """Initialize Flask app and declare variables to
        be used before running every test"""

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.content_type = "application/json"

        # Create all tables
        create_tables()

        self.product = {
            'name': 'Popcorn',
            'category': 'Snacks',
            'quantity': 150,
            "minimum_inventory_quantity": 5,
            'price': 20}

    def tearDown(self):
        """Empty the product dictionary after running every test"""

        self.product = {}
        # Delete all tables
        delete_tables()

    def test_add_a_product(self):
        """Test that a product can be added"""

        response = self.client.post(
            '/api/v2/products',
            data=json.dumps(
                self.product),
            content_type=self.content_type)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"message": "Product has been added"})

    def test_same_product_cant_be_added_again(self):
        """Test same product can't be added again"""

        response1 = self.client.post(
            "/api/v2/products",
            data=json.dumps(
                self.product),
            content_type=self.content_type)
        data = json.loads(response1.get_data().decode('UTF-8'))
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data, {"message": "Product has been added"})

        response2 = self.client.post(
            "/api/v2/products",
            data=json.dumps(
                self.product),
            content_type=self.content_type)
        data = json.loads(response2.get_data().decode('UTF-8'))
        self.assertEqual(response2.status_code, 202)
        self.assertEqual(data, {"message": "Product Popcorn already exists."})
