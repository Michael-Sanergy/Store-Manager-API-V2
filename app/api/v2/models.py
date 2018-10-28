from flask_bcrypt import Bcrypt

# Local import
from .database import db, curr


class UserModel:
    """Model for users"""

    def __init__(self, name, email, phone, password):
        #self.db = init_db()
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

    def validate_password(self, password):
        """check if the hashed password is the same as the password entered by the user"""
        return Bcrypt().check_password_hash(self.password, password)

    @classmethod
    def get_a_user_by_email(cls, email):
        """Search for a user by their email address"""

        query = "SELECT * FROM users WHERE email='{}';".format(email)

        # Execute the query
        curr.execute(query)

        # Get a single user
        user = curr.fetchone()
        return user
