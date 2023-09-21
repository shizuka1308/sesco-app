
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