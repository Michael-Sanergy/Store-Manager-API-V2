from flask_bcrypt import Bcrypt

# Local import
from .database import db, curr


class UserModel:
    """Model for users"""

    def __init__(self, name, email, phone, role, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def signup_user(self):
        """Sign up users"""

        query = """INSERT INTO users (name,email,phone,role,password) VALUES
        ('%s', '%s', '%s', '%s', '%s')""" % (
            self.name, self.email, self.phone, self.role, self.password)

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

    products_list = []

    def __init__(self, data):
        """Initialize class constructor with product details"""

        self.name = data['name']
        self.category = data['category']
        self.quantity = data['quantity']
        self.minimum_inventory_quantity = data['minimum_inventory_quantity']
        self.price = data['price']

    def create_product(self):
        """Create a product"""

        query = """INSERT INTO products (name,category,quantity,minimum_inventory_quantity,price) VALUES
        ('%s', '%s', '%s', '%s', '%s')""" % (self.name, self.category, self.quantity,
                                             self.minimum_inventory_quantity, self.price)

        # Execute the query
        curr.execute(query)

        # Commit changes to database
        db.commit()

    def get_all_products(self):
        """Get all products"""

        query = "SELECT * FROM products"

        # Execute the query
        curr.execute(query)

        products_list = curr.fetchall()
        return products_list

    def get_product_details(self, product):
        """Return the product as a dictionary"""

        return dict(
            id=product[0],
            name=product[1],
            category=product[2],
            quantity=product[3],
            minimum_inventory_quantity=product[4],
            price=product[5])

    @classmethod
    def get_a_product_by_name(cls, name):
        """Search for a product by name"""

        query = "SELECT * FROM products WHERE name='{}';".format(name)

        # Execute the query
        curr.execute(query)

        # Get a single product
        product = curr.fetchone()
        return product

    def get_a_product_by_id(self, id):
        """Search for a product by id"""

        query = "SELECT * FROM products WHERE id={};".format(id)

        # Execute the query
        curr.execute(query)

        # Get a single user
        product = curr.fetchone()
        return product

    def edit_product(self, product_id):
        """Edit a product"""

        curr.execute(
            """UPDATE products SET name = %s, category = %s,quantity=%s,
                minimum_inventory_quantity = %s, price = %s
                WHERE id = %s""", (self.name, self.category, self.quantity,
                                   self.minimum_inventory_quantity, self.price,
                                   product_id),
        )

        # Commit changes to database
        db.commit()