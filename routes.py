# routes.py
# Import the Flask Blueprint class and other necessary modules
from flask import Blueprint, Flask, request, jsonify
from database import (
    get_all_reactors,
    get_reactor_details,
    list_reactors_on_outage_query,
    get_last_known_outage_date,
    get_reactor_by_license_number,
)
from utilities import is_empty_or_whitespace, is_valid_date_format
from errors import (
    INVALID_REACTOR_NAME,
    INVALID_REACTOR_NAME_TYPE,
    REACTOR_NOT_FOUND,
    INVALID_STATE,
    INVALID_STATE_TYPE,
    INVALID_LICENSE_NUMBER,
    INVALID_LICENSE_NUMBER_TYPE,
    INVALID_DATE_FORMAT,
)

routes = Blueprint('routes', __name__)
# API endpoint to retrieve all reactors
@routes.route('/reactors/all', methods=['GET'])
def get_all_reactors_route():
    reactors = get_all_reactors()
    if reactors:
        return jsonify(reactors)
    else:
        return jsonify(REACTOR_NOT_FOUND), 404

# API endpoint to retrieve reactor details by name
@routes.route('/reactors/details', methods=['GET'])
def get_reactor_details_route():
    reactor_name = request.args.get('reactor_name')
    if is_empty_or_whitespace(reactor_name):
        return jsonify(INVALID_REACTOR_NAME), 400

    if not isinstance(reactor_name, str):
        return jsonify(INVALID_REACTOR_NAME_TYPE), 400

    reactor = get_reactor_details(reactor_name)
    if reactor:
        return jsonify(reactor)
    else:
        return jsonify(REACTOR_NOT_FOUND), 404

# API endpoint to filter reactors by state
@routes.route('/reactors/filter', methods=['GET'])
def filter_reactors_by_state_route():
    state = request.args.get('state')
    if is_empty_or_whitespace(state):
        return jsonify(INVALID_STATE), 400

    if not isinstance(state, str):
        return jsonify(INVALID_STATE_TYPE), 400

    reactors = get_all_reactors(state)
    if reactors:
        return jsonify(reactors)
    else:
        return jsonify(REACTOR_NOT_FOUND), 404

# API endpoint to retrieve reactor details by license number
@routes.route('/reactors/license', methods=['GET'])
def get_reactor_by_license_number_route():
    license_number = request.args.get('license_number')
    if is_empty_or_whitespace(license_number):
        return jsonify(INVALID_LICENSE_NUMBER), 400

    if not isinstance(license_number, str):
        return jsonify(INVALID_LICENSE_NUMBER_TYPE), 400

    reactor = get_reactor_by_license_number(license_number)
    if reactor:
        return jsonify(reactor)
    else:
        return jsonify(REACTOR_NOT_FOUND), 404

# API endpoint to filter reactors on outage by date range
@routes.route('/reactors/on_outage/filter', methods=['GET'])
def filter_reactors_on_outage_by_date_route():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not (is_valid_date_format(start_date) and is_valid_date_format(end_date)):
        return jsonify(INVALID_DATE_FORMAT), 400

    reactors_on_outage = list_reactors_on_outage_query(start_date, end_date)
    return jsonify(reactors_on_outage)

# API endpoint to get the last known outage date of a reactor
@routes.route('/reactors/last_known_outage', methods=['GET'])
def get_last_known_outage_date_for_reactor_route():
    reactor_name = request.args.get('reactor_name')
    if is_empty_or_whitespace(reactor_name):
        return jsonify(INVALID_REACTOR_NAME), 400

    if not isinstance(reactor_name, str):
        return jsonify(INVALID_REACTOR_NAME_TYPE), 400

    last_known_outage_date = get_last_known_outage_date(reactor_name)
    if last_known_outage_date:
        return jsonify(last_known_outage_date)
    else:
        return jsonify(REACTOR_NOT_FOUND), 404