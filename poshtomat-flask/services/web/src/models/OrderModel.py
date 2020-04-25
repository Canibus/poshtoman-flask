from marshmallow import fields, Schema
import datetime
from . import bcrypt, db

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    timeUp = db.Column(db.DateTime)
    timeDowm = db.Column(db.DateTime)
    courierId = db.Column(db.Integer, db.ForeignKey('couriers.id'))
    postMachineId = db.Column(db.Integer, db.ForeignKey('post_machines.id'))
    #добавить clientId?
    clientPhone = db.Column(db.String(128), nullable=False)
    orderTime = db.Column(db.DateTime)

    def __init__(self, data):
        self.orderTime = datetime.datetime.utcnow()
        self.clientPhone = data.get('clientPhone')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod 
    def get_one_order(id):
        return Order.query.get(id)

class Orderchema(Schema):
    id = fields.Int(dump_only=True)
    timeUp = fields.Date()
    timeDowm = fields.Date()
    courierId = fields.Int(dump_only=True)
    postMachineId = fields.Int(dump_only=True)
    clientPhone = fields.Str(required=True)
    orderTime = fields.Date()