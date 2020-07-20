from flask import request, json, Response, Blueprint, g
from ..models import CellModel, CellSchema
from ..shared.Authentication import AuthAdmin
from ..shared.Authentication import AuthCli
import requests

cell_api = Blueprint('cells', __name__)
cell_schema = CellSchema(unknown='EXCLUDE')

@cell_api.route('/pm=<int:pm_id>', methods=['GET'])
@AuthAdmin.auth_required
def get_pm_cells(pm_id):
    """
    Get all pm cells
    """
    cells = CellModel.get_all_pm_cells(pm_id)
    if not cells:
        return custom_responce({'error': 'pm not found'}, 404)
    
    ser_cells = cell_schema.dump(cells)
    return custom_responce(ser_order, 200)

@cell_api.route('/free', methods=['GET'])
@AuthCli.auth_required
def get_free_cells():
    """
    Get all free cells
    """
    cells = CellModel.get_all_pm_cells(pm_id)
    if not cells:
        return custom_responce({'error': 'pm not found'}, 404) #######################!!!!!!!!!
    
    ser_cells = cell_schema.dump(cells)
    return custom_responce(ser_order, 200)

# @cell_api.route('/', methods=['GET'])
# @AuthAdmin.auth_required
# def get_all():
#     """
#     Get all places
#     """    
#     places = PlaceModel.get_all_places()
#     ser_places = cell_schema.dump(places, many=True)
#     return custom_responce(ser_places, 200)

# @cell_api.route('/<int:place_id>', methods=['GET'])
# @AuthAdmin.auth_required
# def get_a_place(place_id):
#     """
#     Get a single place
#     """
#     place = PlaceModel.get_one_place(place_id)
#     if not place:
#         return custom_responce({'error': 'place not found'}, 404)
    
#     ser_place = cell_schema.dump(place)
#     return custom_responce(ser_place, 200)

# @cell_api.route('/<int:place_id>', methods=['DELETE'])
# @AuthAdmin.auth_required
# def delete(place_id):
#     """
#     Delete a place
#     """
#     place = PlaceModel.get_one_place(place_id)
#     place.delete()
#     return custom_responce({'message': 'deleted'}, 204)#add responce

# @cell_api.route('/<int:place_id>', methods=['PUT'])
# @AuthAdmin.auth_required
# def update(place_id):
#     """
#     Update place
#     """
#     req_data = request.get_json()
#     data = cell_schema.load(req_data, partial=True)

#     place = PlaceModel.get_one_place(req_data.get('id'))
#     place.update(data)
#     ser_place = cell_schema.dump(place)
#     return custom_responce(ser_place, 200)

# @cell_api.route('/<int:place_id>/pms', methods=['GET'])
# @AuthAdmin.auth_required
# def get_pms(place_id):
#     """
#     Get place pms
#     """
#     place = PlaceModel.get_one_place(place_id)
#     ser_pms = cell_schema.dump(place)["pms"]
#     return custom_responce(ser_pms, 200)


def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
