import json
from flask import make_response, jsonify, request, Blueprint
from app.api.v1.models.seek_services import SeekServicesModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.add_services import AddServicesModel
from utils.v1.validations import check_seek_services_keys, raise_error, convert_to_int
from flask_jwt_extended import jwt_required

seek_services_v1 = Blueprint('seek_services_v1', __name__)


@seek_services_v1.route('/seek_services', methods=['POST'])
@jwt_required
def seek_service():
    """A registered user can seek a service."""
    errors = check_seek_services_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    service_seeker = details['service_seeker']
    service = details['service']
    cost = details['cost']

    value = convert_to_int(service_seeker)
    value2 = convert_to_int(service)
    if type(value) is not int:
        return raise_error(400, "only positive integer is accepted")
    if type(value2) is not int:
        return raise_error(400, "only positive integer is accepted")

    if UsersModel().get_username(service_seeker):
        if AddServicesModel().get_service(service):
            service = SeekServicesModel(service_seeker, service, cost).save()
            return make_response(jsonify({
                "status": "201",
                "message": "You have successfully booked the service!",
                "service": service
            }), 201)
        return raise_error(400, "Please check your input and try again!")
    return raise_error(400, "Please check your input and try again!")

@seek_services_v1.route('/seek_services', methods=['GET'])
@jwt_required
def get_all_services():
    '''Fetch all the existing services.'''

    return make_response(jsonify({
        "status": "200",
        "message": "success",
        "hotels": json.loads(SeekServicesModel().get_services())
    }), 200)

@seek_services_v1.route('/seek_services/<int:service>', methods=['GET'])
@jwt_required
def get_specific_service(service):
    """Fetch a specific service."""

    service = SeekServicesModel().get_service(service)
    service = json.loads(service)
    if service:
        return make_response(jsonify({
            "status": "200",
            "message": "success",
            "service": service
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "service not found"
        }), 404)
