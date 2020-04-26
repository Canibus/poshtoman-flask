from .UserModel import UserModel
from marshmallow import fields, Schema


class CourierModel(UserModel):
    #miss db.Model inheritence
    __tablename__ = "couriers"

    #данные для курьеров

    @staticmethod
    def get_all_couriers():
        return Courier.query.all()
    
    @staticmethod 
    def get_one_courier(id):
        return Courier.query.get(id)
    
class CourierSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)