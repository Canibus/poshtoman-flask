from flask import request, json, Response, Blueprint, g
from ..models import WebAdminModel, WebAdminSchema
from ..shared.Authentication import AuthAdmin

admin_api = Blueprint('admins', __name__)
admin_schema = WebAdminSchema(unknown='EXCLUDE')


# @admin_api.route('/register', methods=['POST'])
# def create():
#     """
#     Create a single admin
#     """
#     req_data = request.get_json()
#     data = admin_schema.load(req_data)

#     admin = WebAdminModel(data)
#     admin.save()
#     ser_data = admin_schema.dump(admin)
#     token = AuthAdmin.generate_token(ser_data.get('id'))#send id from __repr
#     return custom_responce({'jwt_token': token}, 201) 


@admin_api.route('/login', methods=['POST'])
def login():
    """
    AdminModel Login Function
    """
    req_data = request.get_json()
    data = admin_schema.load(req_data, partial=True)

    admin = WebAdminModel.get_admin_by_login(data.get('login'))
    if not admin:
        return custom_responce({'error': 'invalid login'}, 400)
    if not admin.check_hash(data.get('password')):
        return custom_responce({'error': 'invalid password'}, 400)
    ser_data = admin_schema.dump(admin)
    token = AuthAdmin.generate_token(ser_data.get('id'))
    return custom_responce({'jwt_token': token}, 200)

def custom_responce(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
