from marshmallow import fields, Schema
import datetime
from . import bcrypt, db

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    time_up = db.Column(db.DateTime)
    time_down = db.Column(db.DateTime)
    courier_id = db.Column(db.Integer, db.ForeignKey('couriers.id'))
    postmachine_id = db.Column(db.Integer, db.ForeignKey('post_machines.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    order_time = db.Column(db.DateTime)
    comment = db.Column(db.String(128))

    def __init__(self, data):
        self.order_time = datetime.datetime.utcnow()
        self.client_id = data.get('client_id')
        self.postmachine_id = data.get('postmachine_id')
        self.client_id = data.get('client_id')
        self.comment = data.get('comment')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
    @staticmethod
    def get_all_orders():
        return OrderModel.query.all()

    @staticmethod 
    def get_one_order(id):
        return OrderModel.query.get(id)

    @staticmethod 
    def get_order_by_courier_id(courier_id):
        return OrderModel.query.filter(OrderModel.courier_id==courier_id)
    @staticmethod 
    def get_free_order():
        return OrderModel.query.filter(OrderModel.courier_id==None)

class OrdersSchema(Schema):
    id = fields.Int(dump_only=True)
    time_up = fields.DateTime(format='%Y-%m-%d|%H:%M', allow_none=True)
    time_down = fields.DateTime(format='%Y-%m-%d|%H:%M', allow_none=True)
    courier_id = fields.Int(allow_none=True)
    postmachine_id = fields.Int(allow_none=True)
    client_id = fields.Int()
    order_time = fields.DateTime(format='%Y-%m-%d|%H:%M')
    comment = fields.Str(allow_none=True)