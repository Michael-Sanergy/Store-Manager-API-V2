from flask import request
from flask_restplus import Resource, Namespace, fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Local imports
from .models import UserModel, ProductModel

namespace_1 = Namespace("auth/signup", description="End point for signup")
namespace_2 = Namespace("auth/login", description="End point for login")
namespace_3 = Namespace("products", description="End points for products")

user = namespace_1.model('User Registration', {
    'name': fields.String(required=True, description="Your name"),
    'email': fields.String(required=True, description="Your email"),
    'phone': fields.Integer(required=True, description="Phone number"),
    'role': fields.String(required=True, description="Enter 'admin' or 'attendant' role"),
    'password': fields.String(required=True, description="Enter password")
})

user_login = namespace_2.model('User Login', {
    'email': fields.String(required=True, description="Your email"),
    'password': fields.String(required=True, description="Your password")
})

product = namespace_3.model(
    'Products', {
        "name": fields.String(
            required=True, description="Product name"), "category": fields.String(
                required=True, description="Product category"), "quantity": fields.Integer(
                    required=True, description="Quantity"), "minimum_inventory_quantity": fields.Integer(
                        required=True, description="Mininum Inventory Quantity"), "price": fields.Integer(
                            required=True, description="Price")})


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
                data['role'],
                data['password'])

            # Sign up the user
            user.signup_user()
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
                # Create access token
                access_token = create_access_token(identity=data['email'])

                return {"message": "Login Successful",
                        "access_token": access_token}, 201
            return {"message": "Login Failed!"}, 401
        elif not user_record:
            return {"message": "You are not registered!. Please register"}, 403


@namespace_3.route('/')
class ProductView(Resource):
    """Products resource"""

    @jwt_required
    @namespace_3.expect(product)
    def post(self):
        """Add a product"""

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]

        # Check if user is an admin
        if role != 'admin':
            return {"message": "Permission denied! You are not an admin."}, 403

        data = request.get_json(force=True)

        # search the product by id
        product_record = ProductModel.get_a_product_by_name(data['name'])

        # check if the product already exists
        if product_record:
            return {
                "message": "Product {} already exists.".format(
                    data['name'])}, 202

        # create a product if it doesn't exist
        if not product_record:
            product = ProductModel(data)

            # Create the product
            product.create_product()
            return{"message": "Product has been added"}, 201

    @jwt_required
    def get(self):
        """Get all products"""

        products_list = []

        products = ProductModel.get_all_products(self)

        # Check if products exist
        if products is None:
            return {"message": "No products were found"}, 404

        # Loop through all the products
        for p in products:
            products_list.append(ProductModel.get_product_details(self, p))
        return {"message": "Product(s) Found", "data": products_list}, 200


@namespace_3.route('/<int:id>')
class Product(Resource):

    @jwt_required
    def get(self, id):
        """Get a product by id"""

        products_list = []

        # search the product by id
        product = ProductModel.get_a_product_by_id(self, id)

        # Check if product doesn't exist
        if product is None:
            return {"Message": "Product not found"}, 404

        products_list.append(ProductModel.get_product_details(self, product))
        return {"message": "Product Found", "data": products_list}, 200
