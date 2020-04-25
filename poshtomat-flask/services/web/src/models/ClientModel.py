from .UserModel import UserModel
from marshmallow import fields, Schema


class ClientModel(UserModel):
    #miss db.Model inheritence
    __tablename__ = "clients"

    @staticmethod
    def get_all_clients():
        return ClientModel.query.all()
    
    @staticmethod 
    def get_one_client(id):
        return ClientModel.query.get(id)
    
    @staticmethod
    def get_client_by_email(value):
        return ClientModel.query.filter_by(email=value).first()

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
