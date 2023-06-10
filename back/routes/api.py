from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from back.Models import ApiModel
from back.Schemas import ApiSchema

api = Blueprint('api', __name__)


@api.route('/infos', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': ApiSchema
        }
    }
})

def infos():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = ApiModel()
    return ApiSchema().dump(result), 200