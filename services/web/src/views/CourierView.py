from flask import request, json, Response, Blueprint, g
from ..models import CourierModel, CourierSchema
from ..shared.Authentication import Auth

courier_api = Blueprint('couriers', __name__)
couriers_schema = CourierSchema(unknown='EXCLUDE')


@courier_api.route('/', methods=['POST'])
def create():
    """
    Create a single courier
    """
    req_data = request.get_json()
    data = couriers_schema.load(req_data)

    courier_in_db = CourierModel.get_courier_by_phone(data.get('phone'))
    if courier_in_db:
        message = {'error': 'courier already exist, please supply another phone number'}
        return custom_responce(message, 400)
        

    courier = CourierModel(data)
    courier.save()
    ser_data = couriers_schema.dump(courier)
    token = Auth.generate_token(ser_data.get('id'))#send id from __repr
    return custom_responce({'jwt_token': token}, 201) 

@courier_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get all couriers
    """    
    couriers = CourierModel.get_all_couriers()
    ser_couriers = couriers_schema.dump(couriers, many=True)
    return custom_responce(ser_couriers, 200)

@courier_api.route('/<int:courier_id>', methods=['GET'])
@Auth.auth_required
def get_a_courier(courier_id):
    """
    Get a single courier
    """
    courier = CourierModel.get_one_courier(courier_id)
    if not courier:
        return custom_responce({'error': 'courier not found'}, 404)
    
    ser_courier = couriers_schema.dump(courier)
    return custom_responce(ser_courier, 200)

@courier_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data = couriers_schema.load(req_data, partial=True)

    courier = CourierModel.get_one_courier(g.courier.get('id'))
    courier.update(data)
    ser_courier = couriers_schema.dump(courier)
    return custom_responce(ser_courier, 200)

@courier_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a courier
    """
    courier = CourierModel.get_one_courier(g.courier.get('id'))
    courier.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

@courier_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    courier = CourierModel.get_one_courier(g.courier.get('id'))
    ser_courier = couriers_schema.dump(courier)
    return custom_responce(ser_courier, 200)

@courier_api.route('/login', methods=['POST'])
def login():
    """
    CourierModel Login Function
    """
    req_data = request.get_json()

    data = couriers_schema.load(req_data, partial=True)#partial?

    
    if not data.get('email') or not data.get('password'):
        return custom_responce({'error': 'you need email and password to sign in'}, 400)
    courier = CourierModel.get_courier_by_email(data.get('email'))
    if not courier:
        return custom_responce({'error': 'invalid credentials'}, 400)
    if not courier.check_hash(data.get('password')):
        return custom_responce({'error': 'invalid credentials'}, 400)
    ser_data = couriers_schema.dump(courier)
    token = Auth.generate_token(ser_data.get('id'))
    return custom_responce({'jwt_token': token}, 200)

@courier_api.route('/orders', methods=['GET'])
@Auth.auth_required
def get_orders():
    """
    Get orders
    """
    courier = CourierModel.get_one_courier(g.courier.get('id'))
    ser_orders = couriers_schema.dump(courier)["orders"]
    return custom_responce(ser_orders, 200)

def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
