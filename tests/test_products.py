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
        self.header_content = {"content_type": "application/json"}

        # Create all tables
        create_tables()

        self.admin_user = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "7262123",
            "role": "admin",
            "password": "12345"}

        self.admin_login = {
            "email": "johndoe@gmail.com",
            "password": "12345"}

        self.product = {
            'name': 'Popcorn',
            'category': 'Snacks',
            'quantity': 150,
            "minimum_inventory_quantity": 5,
            'price': 20}

        # Sign up admin user
        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.admin_user),
            headers=self.header_content)

        # Login admin user
        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(
                self.admin_login),
            headers=self.header_content)
        result = json.loads(response.data.decode())
        # Get access token
        token = result['access_token']
        self.authorize_user = {"content_type": "application/json"}
        self.authorize_user["Authorization"] = 'Bearer ' + token

    def tearDown(self):
        """Empty the product dictionary after running every test"""

        self.admin_user = {}
        self.admin_login = {}
        self.product = {}
        # Delete all tables
        delete_tables()

    def test_add_a_product(self):

        response = self.client.post(
            '/api/v2/products',
            data=json.dumps(
                self.product),
            headers=self.authorize_user)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"message": "Product has been added"})

    def test_same_product_cant_be_added_again(self):
        """Test same product can't be added again"""

        response1 = self.client.post(
            '/api/v2/products',
            data=json.dumps(
                self.product),
            headers=self.authorize_user)

        data = json.loads(response1.get_data().decode('UTF-8'))
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data, {"message": "Product has been added"})

        response2 = self.client.post(
            '/api/v2/products',
            data=json.dumps(
                self.product),
            headers=self.authorize_user)
        data = json.loads(response2.get_data().decode('UTF-8'))
        self.assertEqual(response2.status_code, 202)
        self.assertEqual(data, {"message": "Product Popcorn already exists."})

    def test_get_all_products(self):
        """Test getting all products"""

        response = self.client.get(
            "/api/v2/products",
            headers=self.authorize_user)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"message": "Product(s) Found", "data": []})
