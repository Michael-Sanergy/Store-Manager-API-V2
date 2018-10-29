from flask import request
from flask_restplus import Resource, Namespace, fields
from flask_bcrypt import Bcrypt

# Local imports
from .models import UserModel

namespace_1 = Namespace("auth/signup", description="End point for signup")
namespace_2 = Namespace("auth/login", description="End point for login")

user = namespace_1.model('User Registration', {
    'name': fields.String(required=True, description="Your name"),
    'email': fields.String(required=True, description="Your email"),
    'phone': fields.Integer(required=True, description="Phone number"),
    'is_admin': fields.Boolean(description="Has admin role"),
    'password': fields.String(required=True, description="Enter password")
})

user_login = namespace_2.model('User Login', {
    'email': fields.String(required=True, description="Your email"),
    'password': fields.String(required=True, description="Your password")
})


@namespace_1.route('/')
class Signup(Resource):
    """The signup resource"""

    @namespace_1.expect(user)
    def post(self):
        """Sign up a user"""

        data = request.get_json(force=True)

        # search the user by email
        user_record = UserModel.get_a_user_by_email(data['email'])

        # check if the user is already registered
        if user_record:
            return {
                "message": "User {} already exists.".format(
                    data['name'])}, 202

        # register the user if he/she isn't registered
        if not user_record:
            user = UserModel(
                data['name'],
                data['email'],
                data['phone'],
                data['password'])

            # Sign up the user
            user.signup_user()
            # UserModel.registered_users.append(signup_user)
            return {"message": "Sign up was successful"}, 201


@namespace_2.route('/')
class Login(Resource):
    """User Login"""

    @namespace_2.expect(user_login)
    def post(self):
        """Login in a user"""

        data = request.get_json(force=True)

        # search the user by email
        user_record = UserModel.get_a_user_by_email(data['email'])

        # check if the user is already registered
        if user_record:
            # Check if hashed password matches the password supplied by user
            validate_password = Bcrypt().check_password_hash(
                user_record[5], data['password'])
            # Check if the login credentials are valid
            if user_record[2] == data['email'] and validate_password:
                return {"message": "Login Successful"}, 201
            return {"message": "Login Failed!"}, 401
        elif not user_record:
            return {"message": "You are not registered!. Please register"}, 403
