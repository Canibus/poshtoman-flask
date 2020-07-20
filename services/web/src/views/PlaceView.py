from flask import request, json, Response, Blueprint, g
from ..models import PlaceModel, PlaceSchema
from ..shared.Authentication import AuthAdmin

place_api = Blueprint('places', __name__)
place_schema = PlaceSchema(unknown='EXCLUDE')

@place_api.route('/', methods=['POST'])
@AuthAdmin.auth_required
def create():
    """
    Create a single place
    """
    req_data = request.get_json()
    data = place_schema.load(req_data)
    place = PlaceModel(data)
    place.save()
    ser_data = place_schema.dump(place)

    return custom_responce(ser_data, 201) 

@place_api.route('/', methods=['GET'])
@AuthAdmin.auth_required
def get_all():
    """
    Get all places
    """    
    places = PlaceModel.get_all_places()
    ser_places = place_schema.dump(places, many=True)
    return custom_responce(ser_places, 200)

@place_api.route('/<int:place_id>', methods=['GET'])
@AuthAdmin.auth_required
def get_a_place(place_id):
    """
    Get a single place
    """
    place = PlaceModel.get_one_place(place_id)
    if not place:
        return custom_responce({'error': 'place not found'}, 404)
    
    ser_place = place_schema.dump(place)
    return custom_responce(ser_place, 200)

@place_api.route('/<int:place_id>', methods=['DELETE'])
@AuthAdmin.auth_required
def delete(place_id):
    """
    Delete a place
    """
    place = PlaceModel.get_one_place(place_id)
    place.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

@place_api.route('/<int:place_id>', methods=['PUT'])
@AuthAdmin.auth_required
def update(place_id):
    """
    Update place
    """
    req_data = request.get_json()
    data = place_schema.load(req_data, partial=True)

    place = PlaceModel.get_one_place(req_data.get('id'))
    place.update(data)
    ser_place = place_schema.dump(place)
    return custom_responce(ser_place, 200)

@place_api.route('/<int:place_id>/pms', methods=['GET'])
@AuthAdmin.auth_required
def get_pms(place_id):
    """
    Get place pms
    """
    place = PlaceModel.get_one_place(place_id)
    ser_pms = place_schema.dump(place)["pms"]
    return custom_responce(ser_pms, 200)


def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
