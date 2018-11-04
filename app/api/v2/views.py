from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .utils import validate_registration, validate_email, validate_product, validate_sale

# Local imports
from .models import UserModel, ProductModel, SaleModel
from .database import db, curr

namespace_1 = Namespace("auth/signup", description="End point for signup")
namespace_2 = Namespace("auth/login", description="End point for login")
namespace_3 = Namespace("products", description="End points for products")
namespace_4 = Namespace("sales", description="End points for sales")

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

sale = namespace_4.model('Sales', {
    'product_name': fields.String(required=True, description="Product Name"),
    'quantity_sold': fields.Integer(required=True, description="Quantity to sell")
})


@namespace_1.route('/')
class Signup(Resource):
    """The signup resource"""

    @namespace_1.expect(user)
    def post(self):
        """Sign up a user"""

        data = request.get_json(force=True)

        if validate_registration(data):
            return validate_registration(data)

        if validate_email(data['email']):
            return {"message": "This email is invalid!"}, 401

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

        if validate_email(data['email']):
            return {"message": "This email is invalid!"}, 401

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
                response_message = {
                    "message": "Logged in as {}".format(
                        user_record[1]),
                    "Authorization": "Bearer " +
                    access_token}
                return response_message, 200
            return {"message": "Login Failed!"}, 401
        elif not user_record:
            return {"message": "You are not registered!. Please register"}, 403


@namespace_3.route('/')
class ProductView(Resource):
    """Products resource"""

    @jwt_required
    @namespace_3.expect(product)
    @namespace_3.doc(security='apikey')
    def post(self):
        """Add a product"""

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]

        # Check if user is an admin
        if role != 'admin':
            return {"message": "Permission denied! You are not an admin."}, 401

        data = request.get_json(force=True)

        if validate_product(data):
            return validate_product(data)

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
    @namespace_3.doc(security='apikey')
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
    @namespace_3.doc(security='apikey')
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

    @jwt_required
    @namespace_3.doc(security='apikey')
    def put(self, id):
        """Get a product by id to edit"""

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]

        # Check if user is an admin
        if role != 'admin':
            return {"message": "Permission denied! You are not an admin."}, 401

        data = request.get_json(force=True)

        if validate_product(data):
            return validate_product(data)

        # Edit the product
        new_product = ProductModel(data)
        new_product.edit_product(id)

        return {"message": "Product was updated successfully"}, 200

    @jwt_required
    @namespace_3.doc(security='apikey')
    def delete(self, id):
        """Delete a product by id"""

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]

        # Check if user is an admin
        if role != 'admin':
            return {"message": "Permission denied! You are not an admin."}, 401

        # search the product by id
        product = ProductModel.get_a_product_by_id(self, id)

        # Check if product doesn't exist
        if product is None:
            return {"Message": "Product not found"}, 404

        data = request.get_json(force=True)

        # Delete Product
        new_product = ProductModel(data)
        new_product.delete_product(id)

        return {"message": "Product deleted"}, 200


@namespace_4.route('/')
class SaleView(Resource):
    """Sales resource"""

    @jwt_required
    @namespace_4.expect(sale)
    @namespace_4.doc(security='apikey')
    def post(self):
        """Add a sale"""

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]
        attendant_name = logged_in_user[1]

        # Check if user is not an attendant
        if role != 'attendant':
            return {
                "message": "Permission denied! You are not an attendant."}, 401

        data = request.get_json(force=True)

        if validate_sale(data):
            return validate_sale(data)

        # search the product by name
        product_record = ProductModel.get_a_product_by_name(
            data['product_name'])

        # check if product doesn't exist
        if not product_record:
            return {
                "message": "Product {} doesn't exists.".format(
                    data['product_name'])}, 404

        product_quantity = product_record[3]
        minimum_inventory_quantity = product_record[4]
        product_price = product_record[5]

        if data['quantity_sold'] > product_quantity:
            return {
                "message": "You can't sell more {} than we have in stock".format(
                    data['product_name'])}, 400

        if product_quantity == minimum_inventory_quantity:
            return {
                "message": "You have reached the minimum stock limit of {} . Please restock item {}".format(
                    minimum_inventory_quantity, data['product_name'])}, 200

        product_quantity = product_quantity - data['quantity_sold']
        curr.execute(
            """ UPDATE products SET quantity= %s WHERE name =%s""",
            (product_quantity,
             data['product_name']))
        db.commit()

        total_price = product_price * data['quantity_sold']
        query = "INSERT INTO sales(product_name, quantity_sold, total_price,attendant_name) VALUES( %s, %s, %s, %s)"
        payload = (
            data['product_name'],
            data['quantity_sold'],
            total_price,
            attendant_name)
        curr.execute(query, payload)

        return{"message": "Sale has been created successfully"}, 201

    @jwt_required
    @namespace_4.doc(security='apikey')
    def get(self):
        """Get all sales"""

        sales_list = []

        # Get email identity used from the access token
        user_email = get_jwt_identity()
        # search the user by email
        logged_in_user = UserModel.get_a_user_by_email(user_email)
        role = logged_in_user[4]

        # Check if user is not an admin
        if role != 'admin':
            return {"message": "Permission denied! You are not an admin."}, 401

        sales = SaleModel.get_all_sales(self)

        # Check if sales exist
        if sales is None:
            return {"message": "No sales were found"}, 404

        # Loop through all the sales
        for s in sales:
            sales_list.append(SaleModel.get_sale_details(self, s))
        return {"message": "Sale(s) Found", "data": sales_list}, 200


@namespace_4.route('/<int:id>')
class Sale(Resource):

    @jwt_required
    @namespace_4.doc(security='apikey')
    def get(self, id):
        """Get a sale by id"""

        sales_list = []

        # search the sale by id
        sale = SaleModel.get_a_sale_by_id(self, id)

        # Check if sale doesn't exist
        if sale is None:
            return {"Message": "Sale not found"}, 404

        sales_list.append(SaleModel.get_sale_details(self, sale))
        return {"message": "Sale Found", "data": sales_list}, 200
