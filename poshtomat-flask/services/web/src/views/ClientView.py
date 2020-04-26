from flask import request, json, Response, Blueprint, g
from ..models import ClientModel, ClientSchema
from ..shared.Authentication import AuthCli
client_api = Blueprint('clients', __name__)
client_schema = ClientSchema()


@client_api.route('/', methods=['POST'])
def create():
    """
    Create a single client
    """
    req_data = request.get_json()
    data = client_schema.load(req_data)

    client_in_db = ClientModel.get_client_by_email(data.get('email'))
    if client_in_db:
        message = {'error': 'client already exist, please supply another email address'}
        return custom_responce(message, 400)
        

    client = ClientModel(data)
    client.save()
    ser_data = client_schema.dump(client)
    token = AuthCli.generate_token(ser_data.get('id'))#send id from __repr
    return custom_responce({'jwt_token': token}, 201) 

@client_api.route('/', methods=['GET'])
@AuthCli.auth_required
def get_all():
    """
    Get all clients
    """    
    clients = ClientModel.get_all_clients()
    ser_clients = client_schema.dump(clients, many=True)
    return custom_responce(ser_clients, 200)

@client_api.route('/<int:client_id>', methods=['GET'])
@AuthCli.auth_required
def get_a_client(client_id):
    """
    Get a single client
    """
    client = ClientModel.get_one_client(client_id)
    if not client:
        return custom_responce({'error': 'client not found'}, 404)
    
    ser_client = client_schema.dump(client)
    return custom_responce(ser_client, 200)

@client_api.route('/me', methods=['PUT'])
@AuthCli.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data = client_schema.load(req_data, partial=True)

    client = ClientModel.get_one_client(g.client.get('id'))
    client.update(data)
    ser_client = client_schema.dump(client)
    return custom_responce(ser_client, 200)

@client_api.route('/me', methods=['DELETE'])
@AuthCli.auth_required
def delete():
    """
    Delete a client
    """
    client = ClientModel.get_one_client(g.client.get('id'))
    client.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

@client_api.route('/me', methods=['GET'])
@AuthCli.auth_required
def get_me():
    """
    Get me
    """
    client = ClientModel.get_one_client(g.client.get('id'))
    ser_client = client_schema.dump(client)
    return custom_responce(ser_client, 200)

@client_api.route('/login', methods=['POST'])
def login():
    """
    ClientModel Login Function
    """
    req_data = request.get_json()

    data = client_schema.load(req_data, partial=True)#partial?

    
    if not data.get('email') or not data.get('password'):
        return custom_responce({'error': 'you need email and password to sign in'}, 400)
    client = ClientModel.get_client_by_email(data.get('email'))
    if not client:
        return custom_responce({'error': 'invalid credentials'}, 400)
    if not client.check_hash(data.get('password')):
        return custom_responce({'error': 'invalid credentials'}, 400)
    ser_data = client_schema.dump(client)
    token = AuthCli.generate_token(ser_data.get('id'))
    return custom_responce({'jwt_token': token}, 200)

def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
