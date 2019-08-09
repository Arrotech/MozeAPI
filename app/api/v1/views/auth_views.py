import json
from flask import make_response, jsonify, request, Blueprint
import datetime
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.api.v1.models.users_model import UsersModel
from utils.v1.validations import raise_error, check_register_keys, is_valid_email,\
 portfolio_restrictions, is_valid_phone, is_valid_password, check_login_keys

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

@auth_v1.route('/login', methods=['POST'])
def login():
    """Already existing user can sign in to their account."""
    errors = check_login_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    email = details['email']
    password = details['password']

    user = json.loads(UsersModel().get_email(email))
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            expires = datetime.timedelta(days=365)
            token = create_access_token(identity=email, expires_delta=expires)
            refresh_token = create_refresh_token(identity=email, expires_delta=expires)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "token": token,
                "refresh_token": refresh_token,
                "user": user
            }), 200)
        return make_response(jsonify({
            "status": "401",
            "message": "Invalid Email or Password"
        }), 401)
    return make_response(jsonify({
        "status": "401",
        "message": "Invalid Email or Password"
    }), 401)
