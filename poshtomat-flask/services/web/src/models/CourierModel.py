from .UserModel import UserModel
from marshmallow import fields, Schema


class CourierModel(UserModel):
    #miss db.Model inheritence
    __tablename__ = "couriers"

    #данные для курьеров

    @staticmethod
    def get_all_couriers():
        return CourierModel.query.all()
    
    @staticmethod 
    def get_one_courier(id):
        return CourierModel.query.get(id)
    
    @staticmethod
    def get_courier_by_email(value):
        return CourierModel.query.filter_by(email=value).first()

class CourierSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)