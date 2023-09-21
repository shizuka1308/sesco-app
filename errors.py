# errors.py

INVALID_REACTOR_NAME = {"error": "Reactor name is required"}, 400
INVALID_REACTOR_NAME_TYPE = {"error": "Reactor name must be a string"}, 400
REACTOR_NOT_FOUND = {"error": "Reactor not found"}, 404
INVALID_STATE = {"error": "State is required"}, 400
INVALID_STATE_TYPE = {"error": "State must be a string"}, 400
INVALID_LICENSE_NUMBER = {"error": "License Number is required"}, 400
INVALID_LICENSE_NUMBER_TYPE = {"error": "License Number must be a string"}, 400
INVALID_DATE_FORMAT = {"error": "Start date and end date must be in the 'yyyy-mm-dd' format"}, 400
