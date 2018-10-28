from flask import request
from flask_restplus import Resource, Namespace, fields

# Local imports
from .models import UserModel

namespace_1 = Namespace("auth/signup", description="End point for signup")

user = namespace_1.model('User Registration', {
    'name': fields.String(required=True, description="Your name"),
    'email': fields.String(required=True, description="Your email"),
    'phone': fields.Integer(required=True, description="Phone number"),
    'is_admin': fields.Boolean(description="Has admin role"),
    'password': fields.String(required=True, description="Enter password")
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
            return {"message": "User {} already exists.".format(data['name'])}

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
