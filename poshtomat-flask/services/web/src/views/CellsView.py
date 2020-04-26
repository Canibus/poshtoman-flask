from flask import request, json, Response, Blueprint, g
from ..models import CellModel, CellSchema
from ..shared.Authentication import Auth

cell_api = Blueprint('cells', __name__)
cell_schema = CellSchema()


@cell_api.route('/', methods=['POST'])
def create():
    """
    Create a single cell
    """
    req_data = request.get_json()
    data = cell_schema.load(req_data)
    cell = CellModel(data)
    cell.save()
    ser_data = cell_schema.dump(cell)

    return custom_responce(ser_data, 201) 

@cell_api.route('/', methods=['GET'])
#@Auth.auth_required
def get_all():
    """
    Get all cells
    """    
    cells = CellModel.get_all_cells()
    ser_cells = cell_schema.dump(cells, many=True)
    return custom_responce(ser_cells, 200)

@cell_api.route('/<int:cell_id>', methods=['GET'])
#@Auth.auth_required
def get_a_cell(cell_id):
    """
    Get a single cell
    """
    cell = CellModel.get_one_cell(cell_id)
    if not cell:
        return custom_responce({'error': 'cell not found'}, 404)
    
    ser_cell = cell_schema.dump(cell)
    return custom_responce(ser_cell, 200)

@cell_api.route('/<int:cell_id>', methods=['PUT'])
#@Auth.auth_required
def update(cell_id):
    """
    Update cell
    """
    req_data = request.get_json()
    data = cell_schema.load(req_data, partial=True)

    cell = CellModel.get_one_cell(cell_id)
    cell.update(data)
    ser_cell = cell_schema.dump(cell)
    return custom_responce(ser_cell, 200)


@cell_api.route('/<int:cell_id>', methods=['DELETE'])
#@Auth.auth_required
def delete(cell_id):
    """
    Delete a cell
    """
    cell = CellModel.get_one_cell(cell_id)
    cell.delete()
    return custom_responce({'message': 'deleted'}, 204)


def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
