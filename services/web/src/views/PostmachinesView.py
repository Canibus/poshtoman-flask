from flask import request, json, Response, Blueprint, g
from ..models import PostmachineModel, PostmachineSchema
from ..shared.Authentication import AuthAdmin
import requests

pm_api = Blueprint('pms', __name__)
pm_schema = PostmachineSchema(unknown='EXCLUDE')

@pm_api.route('/', methods=['POST'])
@AuthAdmin.auth_required
def create():
    """
    Create a single pm
    """
    req_data = request.get_json()
    data = pm_schema.load(req_data)
    pm = PostmachineModel(data)
    pm.save()
    ser_data = pm_schema.dump(pm)

    res = requests.get(ser_data['url'])

    return custom_responce(ser_data, 201) 

@pm_api.route('/', methods=['GET'])
@AuthAdmin.auth_required
def get_all():
    """
    Get all pms
    """    
    pms = PostmachineModel.get_all_machines()
    ser_pms = pm_schema.dump(pms, many=True)
    return custom_responce(ser_pms, 200)

@pm_api.route('/<int:pm_id>', methods=['GET'])
@AuthAdmin.auth_required
def get_a_pm(pm_id):
    """
    Get a single pm
    """
    pm = PostmachineModel.get_one_machine(pm_id)
    if not pm:
        return custom_responce({'error': 'pm not found'}, 404)
    
    ser_pm = pm_schema.dump(pm)
    return custom_responce(ser_pm, 200)

@pm_api.route('/<int:pm_id>', methods=['PUT'])
@AuthAdmin.auth_required
def update(pm_id):
    """
    Update pm
    """
    req_data = request.get_json()
    data = pm_schema.load(req_data, partial=True)

    pm = PostmachineModel.get_one_machine(req_data.get('id'))
    pm.update(data)
    ser_pm = pm_schema.dump(pm)
    return custom_responce(ser_pm, 200)


@pm_api.route('/<int:pm_id>', methods=['DELETE'])
@AuthAdmin.auth_required
def delete(pm_id):
    """
    Delete a pm
    """
    pm = PostmachineModel.get_one_machine(pm_id)
    pm.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

@pm_api.route('/<int:pm_id>/cells', methods=['GET'])
@AuthAdmin.auth_required
def get_all_cells(pm_id):
    obj = PostmachineModel.get_all_cells_info(pm_id)
    ser = pm_schema.dump(obj)
    res = requests.get(ser['url'])

    return custom_responce(res.json(), 200)

@pm_api.route('/<int:pm_id>/<string:cell_id>/<action>', methods=['GET'])
@AuthAdmin.auth_required
def change_pin_status(pm_id, cell_id, action):
    obj = PostmachineModel.get_all_cells_info(pm_id)
    ser = pm_schema.dump(obj)

    res = requests.get(ser['url'] + '/' + cell_id + '/' + action)
    if res:
        if action == "on":
            return custom_responce("cell " + cell_id + " was opened", 200)
        else:
            return custom_responce("cell " + cell_id + " was closed", 200)
    #return custom_responce(res.json(), 200)

def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
