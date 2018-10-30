from flask_bcrypt import Bcrypt

# Local import
from .database import db, curr


class UserModel:
    """Model for users"""

    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.is_admin = False
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def signup_user(self):
        """Sign up users"""

        query = """INSERT INTO users (name,email,phone,is_admin,password) VALUES
        ('%s', '%s', '%s', '%s', '%s')""" % (
            self.name, self.email, self.phone, self.is_admin, self.password)

        # Execute the query
        curr.execute(query)

        # Commit changes to database
        db.commit()

    @classmethod
    def get_a_user_by_email(cls, email):
        """Search for a user by their email address"""

        query = "SELECT * FROM users WHERE email='{}';".format(email)

        # Execute the query
        curr.execute(query)

        # Get a single user
        user = curr.fetchone()
        return user


class ProductModel:
    """Model for products"""

    def __init__(
            self,
            name,
            category,
            quantity,
            minimum_inventory_quantity,
            price):
        """Initialize class constructor with product details"""

        self.name = name
        self.category = category
        self.quantity = quantity
        self.minimum_inventory_quantity = minimum_inventory_quantity
        self.price = price

    def create_product(self):
        """Create a product"""

        query = """INSERT INTO products (name,category,quantity,minimum_inventory_quantity,price) VALUES
        ('%s', '%s', '%s', '%s', '%s')""" % (self.name, self.category, self.quantity,
                                             self.minimum_inventory_quantity, self.price)

        # Execute the query
        curr.execute(query)

        # Commit changes to database
        db.commit()

    @classmethod
    def get_a_product_by_id(cls, name):
        """Search for a product by name"""

        query = "SELECT * FROM products WHERE name='{}';".format(name)

        # Execute the query
        curr.execute(query)

        # Get a single user
        product = curr.fetchone()
        return product
