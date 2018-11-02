import json
import re


def validate_registration(data):
    """Validate registration of user"""

    if len(data["name"]) == 0 or data["name"] == " ":
        return {"message": "Name is required"}, 400
    if len(data["email"]) == 0 or data["email"] == " ":
        return {"message": "Email is required"}, 400
    if not data["phone"] or data["phone"] == " ":
        return {"message": "Phone no. is required"}, 400
    if len(data["role"]) == 0 or data["role"] == " ":
        return {"message": "Role is required"}, 400
    if len(data["password"]) == 0 or data["password"] == " ":
        return {"message": "Password is required"}, 400
    if not isinstance(data['phone'], int):
        return {"Message": "Phone must be an integer"}, 400


def validate_email(email):
    """Check if the email is valid"""

    # Check if email is valid
    email_format = re.match(
        '^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$',
        email)

    if email_format is None:
        response = True
    else:
        response = False
    return response


def validate_product(data):
    """Validate adding a product"""

    if len(data["name"]) == 0 or data["name"] == " ":
        return {"message": "Name is required"}, 400
    if len(data["category"]) == 0 or data["category"] == " ":
        return {"message": "Category is required"}, 400
    if not data["quantity"] or data["quantity"] == " ":
        return {"message": "Quantity is required"}, 400
    if not data["minimum_inventory_quantity"] or data["minimum_inventory_quantity"] == " ":
        return {"message": "minimum inventory quantity is required"}, 400
    if not data["price"] or data["price"] == " ":
        return {"message": "Price is required"}, 400
    if not isinstance(data['quantity'], int):
        return {"Message": "Quantity must be an integer"}, 400
    if not isinstance(data['minimum_inventory_quantity'], int):
        return {"Message": "Minimum Quantity must be an integer"}, 400
    if not isinstance(data['price'], int):
        return {"Message": "Price must be an integer"}, 400


def validate_sale(data):
    """Validate creating a sale"""

    if not data["quantity_sold"] or data["quantity_sold"] == " ":
        return {"message": "Quantity sold is required"}, 400
    if not isinstance(data['quantity_sold'], int):
        return {"message": "Quantity sold must be an integer"}, 400
    if len(data["product_name"]) == 0 or data["product_name"] == " ":
        return {"message": "Product Name field is required"}, 400
