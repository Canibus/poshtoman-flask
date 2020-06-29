from marshmallow import fields, Schema
from .OrderModel import OrdersSchema, OrderModel
from .PlaceModel import PlaceSchema, PlaceModel
from .RentCellModel import RentedCellSchema, RentedCellModel
from . import db, bcrypt
import datetime 

class ClientModel(db.Model):
    #miss db.Model inheritence
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    patronymic = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    keyword = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.String(128))
    last_activity = db.Column(db.DateTime)
    orders = db.relationship(OrderModel, backref='client', lazy=True)
    #orders = db.relationship('orders', backref='client') was
    #places = db.relationship(PlaceModel, secondary='clients_places', backref=db.backref('clients', lazy='dynamyc')) was
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    #places = db.relationship(PlaceModel, secondary='clients_places', backref=db.backref('clients'), lazy='dynamic')
    cells = db.relationship(RentedCellModel, backref='client')


    def __init__(self, data):
        self.name = data.get('name')
        self.patronymic = data.get('patronymic')
        self.surname = data.get('surname')
        self.phone = data.get('phone')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.keyword = data.get('keyword')
        self.comment = data.get('comment')       
        self.place_id = data.get('place_id')   
        self.last_activity = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
                setattr(self, key, self.password)
            else:
                setattr(self, key, item)
        self.last_activity=datetime.datetime.utcnow()
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):#repl?
        return '<id {}>'.format(self.id)

    @staticmethod
    def get_all_clients():
        return ClientModel.query.all()
    
    @staticmethod 
    def get_one_client(id):
        return ClientModel.query.get(id)
    
    @staticmethod
    def get_client_by_email(value):
        return ClientModel.query.filter_by(email=value).first()
        
    @staticmethod
    def get_client_by_phone(value):
        return ClientModel.query.filter_by(phone=value).first()

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    patronymic = fields.Str()
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    keyword = fields.Str(required=True)
    comment = fields.Str()
    last_activity = fields.DateTime(dump_only=True, format='%Y-%m-%d|%H:%M')
    orders = fields.Nested(OrdersSchema, many=True)
    #places = fields.Nested(PlaceSchema, many=True)
    place_id=fields.Int()
    cells = fields.Nested(RentedCellSchema, many=True)