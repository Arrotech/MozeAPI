import json
from flask import make_response, jsonify, request, Blueprint
from app.api.v1.models.users_model import UsersModel
from utils.v1.validations import raise_error, check_register_keys, is_valid_email, portfolio_restrictions, is_valid_phone, is_valid_password

auth_v1 = Blueprint('auth_v1', __name__)


@auth_v1.route('/register', methods=['POST'])
def signup():
    """A new user can create a new account."""
    errors = check_register_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    surname = details['surname']
    phone = details['phone']
    location = details['location']
    portfolio = details['portfolio']
    occupation = details['occupation']
    username = details['username']
    email = details['email']
    password = details['password']
    cost = details['cost']

    if details['firstname'].isalpha() is False:
        return raise_error(400, "First name is in wrong format")
    if details['lastname'].isalpha() is False:
        return raise_error(400, "Last name is in wrong format")
    if details['surname'].isalpha() is False:
        return raise_error(400, "Surname is in wrong format")
    if (portfolio_restrictions(portfolio) is False):
        return raise_error(400, "Portfolio should be either Education, Technical, Health or Domestic")
    if details['occupation'].isalpha() is False:
        return raise_error(400, "Occupation is in wrong format")
    if not is_valid_phone(phone):
        return raise_error(400, "Invalid phone number!")
    if not is_valid_email(email):
        return raise_error(400, "Invalid email!")
    if not is_valid_password(password):
        return raise_error(400, "Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!")
    if type(cost) != float:
        return raise_error(400, "Invalid cost value!")
    user_phone = json.loads(UsersModel().get_phone(phone))
    if user_phone:
        return raise_error(400, "Phone number already exists!")
    user_username = json.loads(UsersModel().get_username(username))
    if user_username:
        return raise_error(400, "Username already exists!")
    user_email = json.loads(UsersModel().get_email(email))
    if user_email:
        return raise_error(400, "Email already exists!")
    user = UsersModel(firstname, lastname, surname, phone, location, portfolio, occupation, username, email, password, cost).save()
    user = json.loads(user)
    return make_response(jsonify({
        "message": "Account created successfully!",
        "status": "201",
        "user": user
    }), 201)