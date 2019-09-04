import re

from flask import jsonify, make_response


def raise_error(status, msg):
    return make_response(jsonify({
        "status": "400",
        "message": msg
    }), status)

def check_register_keys(request):
    res_keys = ['firstname', 'lastname', 'phone', 'username', 'email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def check_login_keys(request):
    res_keys = [ 'email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def check_add_services_keys(request):
    res_keys = ['service_provider', 'portfolio', 'occupation', 'phone', 'location', 'img', 'cost']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def check_seek_services_keys(request):
    res_keys = ['service_seeker', 'service', 'cost']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors

def convert_to_int(id):
    try:
        value = int(id)
        if value > 0:
            return value
        return raise_error(400, "cannot be a negative number")
    except Exception as e:
        return {"message": e}

def is_valid_email(variable):
    """Check if email is a valid mail."""
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$)",
                variable):
        return True
    return False

def is_valid_phone(variable):
    """Check if email is a valid mail."""
    if re.match(r"(^(?:254|\+254|0)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$)",
                variable):
        return True
    return False

def is_valid_password(variable):
    """Check if password is a valid password."""
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", variable):
        return True
    return False

def portfolio_restrictions(data):
    """Restrict user inputs in a list."""

    form = ["Health", "Technical", "Education", "Domestic"]
    if data not in form:
        return False
    return True
