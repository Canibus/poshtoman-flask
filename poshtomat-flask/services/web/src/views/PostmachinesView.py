from flask import request, json, Response, Blueprint, g
from ..models import PostmachineModel, PostmachineSchema
from ..shared.Authentication import Auth

pm_api = Blueprint('pms', __name__)
pm_schema = PostmachineSchema()


@pm_api.route('/', methods=['POST'])
def create():
    """
    Create a single pm
    """
    req_data = request.get_json()
    data = pm_schema.load(req_data)
    pm = PostmachineModel(data)
    pm.save()
    ser_data = pm_schema.dump(pm)

    return custom_responce(ser_data, 201) 

@pm_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get all pms
    """    
    pms = PostmachineModel.get_all_machines()
    ser_pms = pm_schema.dump(pms, many=True)
    return custom_responce(ser_pms, 200)

@pm_api.route('/<int:pm_id>', methods=['GET'])
@Auth.auth_required
def get_a_pm(pm_id):
    """
    Get a single pm
    """
    pm = PostmachineModel.get_one_machine(pm_id)
    if not pm:
        return custom_responce({'error': 'pm not found'}, 404)
    
    ser_pm = pm_schema.dump(pm)
    return custom_responce(ser_pm, 200)

@pm_api.route('/<int:pm_id>', methods=['DELETE'])
@Auth.auth_required
def delete(pm_id):
    """
    Delete a pm
    """
    pm = PostmachineModel.get_one_machine(pm_id)
    pm.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce


def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
