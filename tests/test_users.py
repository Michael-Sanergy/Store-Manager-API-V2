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

        self.users = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "722123456",
            "is_admin": False,
            "password": "12345"}

        self.user_login = {
            "email": "johndoe@gmail.com",
            "password": "12345"}

    def tearDown(self):
        """Empty the dictionaries and delete tables after running every test"""

        self.users = {}
        self.user_login = {}
        # Delete all tables
        delete_tables()

    def test_admin_can_signup_a_user(self):
        """Test admin can add a user"""

        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"message": "Sign up was successful"})

    def test_admin_cant_signup_same_user_again(self):
        """Test admin can't signup same user again"""

        response1 = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)
        data = json.loads(response1.get_data().decode('UTF-8'))
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data, {"message": "Sign up was successful"})

        response2 = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)
        data = json.loads(response2.get_data().decode('UTF-8'))
        self.assertEqual(response2.status_code, 202)
        self.assertEqual(data, {"message": "User John Doe already exists."})

    def test_registered_user_can_login_with_valid_credentials(self):
        """Test user can login with valid credentials"""

        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)

        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(
                self.user_login),
            content_type=self.content_type)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"message": "Login Successful"})

    def test_registered_user_cant_login_with_wrong_password(self):
        """Test user can't login with wrong password"""

        payload = {
            "email": "johndoe@gmail.com",
            "password": "123xyz"}

        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(
                self.users),
            content_type=self.content_type)

        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(payload),
            content_type=self.content_type)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"message": "Login Failed!"})

    def test_unregistered_user_cant_login(self):
        """Test an unregistered user can't login"""

        payload = {
            "email": "ironman@gmail.com",
            "password": "avengers"}

        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(payload),
            content_type=self.content_type)
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data, {
                "message": "You are not registered!. Please register"})
