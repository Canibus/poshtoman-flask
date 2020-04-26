from flask import request, json, Response, Blueprint, g
from ..models import OrderModel, OrdersSchema
from ..shared.Authentication import Auth, AuthCli

order_api = Blueprint('orders', __name__)
orders_schema = OrdersSchema()

#Clients api

@order_api.route('/', methods=['POST'])
@AuthCli.auth_required
def create():
    """
    Create a single order
    """
    req_data = request.get_json()
    req_data['client_id'] = g.client.get('id')
    data = orders_schema.load(req_data)
        
    order = OrderModel(data)
    order.save()
    ser_data = orders_schema.dump(order)
    return custom_responce(ser_data, 201) 

#just for dev
@order_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get all orders
    """    
    orders = OrderModel.get_all_orders()
    ser_orders = orders_schema.dump(orders, many=True)
    return custom_responce(ser_orders, 200)

@order_api.route('/order=<int:order_id>', methods=['GET'])
@AuthCli.auth_required
def get_a_order(order_id):
    """
    Get a single order
    """
    order = OrderModel.get_one_order(order_id)
    if not order:
        return custom_responce({'error': 'order not found'}, 404)
    
    ser_order = orders_schema.dump(order)
    return custom_responce(ser_order, 200)
'''
@order_api.route('/order=<int:order_id>', methods=['PUT'])
@AuthCli.auth_required
def update(order_id):
    """
    Update me for client
    """
    req_data = request.get_json()
    order = OrderModel.get_one_order(order_id)
    #just left fields for client
    if not order:
        return custom_responce({'error': 'order not found'}, 404)
    data = orders_schema.dump(order)
    data = orders_schema.load(req_data, partial=True)

    order.update(data)
    ser_order = orders_schema.dump(order)
    return custom_responce(ser_order, 200)
'''
@order_api.route('/<int:order_id>', methods=['DELETE'])
@Auth.auth_required
def delete(order_id):
    """
    Delete a order
    """
    order = OrderModel.get_one_order(order_id)
    order.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

#Couriers api

@order_api.route('/courier=<int:courier_id>', methods=['GET'])
@Auth.auth_required
def get_for_id(courier_id):
    """
    Get all orders for courier id
    """    
    orders = OrderModel.get_order_by_courier_id(courier_id)
    ser_orders = orders_schema.dump(orders, many=True)
    return custom_responce(ser_orders, 200)

@order_api.route('/free', methods=['GET'])
@Auth.auth_required
def get_free():
    """
    Get all orders without couriers
    """    
    orders = OrderModel.get_free_order()
    ser_orders = orders_schema.dump(orders, many=True)
    return custom_responce(ser_orders, 200)

@order_api.route('/order_edit=<int:order_id>', methods=['PUT'])
@Auth.auth_required
def update_by_courier(order_id):
    """
    Update order
    """
    req_data = request.get_json()
    order = OrderModel.get_one_order(order_id)

    if not order:
        return custom_responce({'error': 'order not found'}, 404)
    data = orders_schema.dump(order)

    if data.get('courier_id') != None:
        if g.courier.get('id') != data.get('courier_id') and data.get('courier_id') != None:
            return custom_responce({'error': 'this order is busy'}, 400)
        
    data = orders_schema.load(req_data, partial=True)

    order.update(data)
    ser_order = orders_schema.dump(order)
    return custom_responce(ser_order, 200)

def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
