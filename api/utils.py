from flask import jsonify


def create_response(status_code=200, message='', data={}):
    return_data = {
        'data': data,
        'alert': message
    }
    return jsonify(return_data), status_code
