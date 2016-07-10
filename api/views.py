from api import app
from api.utils import create_response
from api.response_codes import response_codes_dict


@app.route('/', methods=['GET'])
def home():
    return create_response(
        status_code=response_codes_dict['success'],
        message='Welcome to the homepage'
    )
