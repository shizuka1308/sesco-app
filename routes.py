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