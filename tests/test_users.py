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
        self.app.config.update(
            DATABASE_URL='postgresql://postgres:12345@localhost:5432/test_db')
        self.client = self.app.test_client()
        self.content_type = "application/json"

        # Create all tables
        create_tables()

        self.users = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "722123456",
            "is_admin": False,
            "password": "12345"}

    def tearDown(self):
        """Empty the dictionary and delete tables after running every test"""

        self.users = {}
        # Delete all tables
        delete_tables()

    def test_admin_can_signup_a_user(self):
        """Test admin can add a user"""

        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)
        self.assertEqual(response.status_code, 201)
