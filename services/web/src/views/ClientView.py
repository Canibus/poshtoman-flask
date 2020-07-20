from flask import request, json, Response, Blueprint, g
from ..models import ClientModel, ClientSchema
from ..shared.Authentication import AuthCli, AuthAdmin
from ..shared.TwilioToken import Token
from ..shared import MailSender
import datetime
from flask_jwt_extended import create_access_token, decode_token

client_api = Blueprint('clients', __name__)
client_schema = ClientSchema(unknown='EXCLUDE')


@client_api.route('/register', methods=['POST'])
def create():
    """
    Create a single client
    """
    req_data = request.get_json()
    data = client_schema.load(req_data, partial=True)

    #проверить
    client_in_db_email = ClientModel.get_client_by_email(data.get('email'))
    client_in_db_phone = ClientModel.get_client_by_phone(data.get('phone'))
    if client_in_db_email:
        message = {'error': 'this email already exist, please supply another email address'}
        return custom_responce(message, 400)
    
    if client_in_db_phone:
        message = {'error': 'this phone already exist, please supply another phone number'}
        return custom_responce(message, 400)
        
    if Token.check_verification_token(req_data.get('phone'), req_data.get('sms')) == False:
        message = {'error': 'invalid sms code'}
        return custom_responce(message, 400)
    client = ClientModel(data)
    client.save()
    ser_data = client_schema.dump(client)
    token = AuthCli.generate_token(ser_data.get('id'))#send id from __repr
    return custom_responce({'jwt_token': token}, 201) 

@client_api.route('/verify', methods=['POST'])
def verify():
    req_data = request.get_json()
    phone_in_db = ClientModel.get_client_by_phone(req_data.get('phone'))
    if phone_in_db:
        return custom_responce({'message': 'this phone already exist, please supply another phone number'}, 400)
    Token.request_verification_token(req_data.get('phone'))
    return custom_responce({'message': 'sms sended'}, 204)

@client_api.route('/reset', methods=['POST'])
def forgot():
    url = request.host_url + 'api/v2/clients/reset/'
    req_data = request.get_json()
    phone_in_db = ClientModel.get_client_by_phone(req_data.get('phone'))
    if not phone_in_db:
        return custom_responce({'message': 'this phone is not exist in our db'}, 400)

    expires = datetime.timedelta(hours=24)
    reset_token = create_access_token(str(phone_in_db.id), expires_delta=expires)
    MailSender.send_to(phone_in_db.email,"follow this link to reset your password: " + url + reset_token)
    return custom_responce({'message': 'email sended'}, 204)

@client_api.route('/reset/<reset_token>', methods=['POST'])
def reset(reset_token):
    req_data = request.get_json()
    req_data['password']

    user_id = decode_token(reset_token)['identity']

    user = ClientModel.get_one_client(user_id)
    user.update(req_data)

    return custom_responce({'message': 'password updated'}, 204)

@client_api.route('/', methods=['GET'])
@AuthAdmin.auth_required
def get_all():
    """
    Get all clients
    """    
    clients = ClientModel.get_all_clients()
    ser_clients = client_schema.dump(clients, many=True)
    return custom_responce(ser_clients, 200)

@client_api.route('/<int:client_id>', methods=['DELETE'])
@AuthAdmin.auth_required
def admin_delete(client_id):
    """
    Delete a client
    """
    client = ClientModel.get_one_client(client_id)
    client.delete()
    return custom_responce({'message': 'deleted'}, 204)#add responce

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

@client_api.route('/<int:client_id>', methods=['PUT'])
@AuthAdmin.auth_required
def update_admin(client_id):
    """
    Update client
    """
    req_data = request.get_json()
    print(req_data)
    data = client_schema.load(req_data, partial=True)

    client = ClientModel.get_one_client(client_id)
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
    if not client:
        return custom_responce({'error': 'could not get user data'}, 400)
    ser_client = client_schema.dump(client)
    return custom_responce(ser_client, 200)

@client_api.route('/login', methods=['POST'])
def login():
    """
    ClientModel Login Function
    """
    req_data = request.get_json()

    data = client_schema.load(req_data, partial=True)

    
    if not data.get('phone') or not data.get('password'):
        return custom_responce({'error': 'you need phone and password to sign in'}, 400)
    client = ClientModel.get_client_by_phone(data.get('phone'))
    if not client:
        return custom_responce({'error': 'invalid credentials'}, 400)
    if not client.check_hash(data.get('password')):
        return custom_responce({'error': 'invalid credentials'}, 400)
    ser_data = client_schema.dump(client)
    token = AuthCli.generate_token(ser_data.get('id'))
    return custom_responce({'jwt_token': token}, 200)

@client_api.route('/orders', methods=['GET'])
@AuthCli.auth_required
def get_orders():
    """
    Get client orders
    """
    client = ClientModel.get_one_client(g.client.get('id'))
    ser_orders = client_schema.dump(client)["orders"]
    return custom_responce(ser_orders, 200)

@client_api.route('/cells', methods=['GET'])
@AuthCli.auth_required
def get_cells():
    """
    Get client cells
    """
    client = ClientModel.get_one_client(g.client.get('id'))
    ser_cells = client_schema.dump(client)["cells"]
    return custom_responce(ser_cells, 200)

@client_api.route('/places', methods=['GET'])
@AuthCli.auth_required
def get_places():
    """
    Get client places
    """
    client = ClientModel.get_one_client(g.client.get('id'))
    ser_places = client_schema.dump(client)["places"]
    return custom_responce(ser_places, 200)



def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
