from .UserModel import UserModel
from marshmallow import fields, Schema
from .OrderModel import OrdersSchema, OrderModel
from . import db

class CourierModel(UserModel):
    #miss db.Model inheritence
    __tablename__ = "couriers"

    orders = db.relationship(OrderModel, backref='courier')

    @staticmethod
    def get_all_couriers():
        return CourierModel.query.all()
    
    @staticmethod 
    def get_one_courier(id):
        return CourierModel.query.get(id)
    
    @staticmethod
    def get_courier_by_email(value):
        return CourierModel.query.filter_by(email=value).first()

    def get_courier_by_phone(value):
        return CourierModel.query.filter_by(phone=value).first()

class CourierSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    patronymic = fields.Str()
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    keyword = fields.Str(required=True, load_only=True)
    comment = fields.Str()
    last_activity = fields.DateTime(dump_only=True)
    orders = fields.Nested(OrdersSchema, many=True)