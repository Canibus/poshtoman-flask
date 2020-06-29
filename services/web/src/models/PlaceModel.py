from marshmallow import fields, Schema
from .PostmachineModel import PostmachineSchema, PostmachineModel
from . import db


class PlaceModel(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    org_name = db.Column(db.String(60))
    bailee = db.Column(db.String(60))
    phone = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.String(128))
    pms = db.relationship(PostmachineModel, backref='pm', lazy=True)
    


    def __init__(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.org_name = data.get('org_name')
        self.bailee = data.get('bailee')
        self.phone = data.get('phone')
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
    
    @staticmethod
    def get_all_places():
        return PlaceModel.query.all()

    @staticmethod 
    def get_one_place(id):
        return PlaceModel.query.get(id)
        


class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    address = fields.String()
    org_name = fields.String()
    bailee = fields.String()
    phone = fields.String()
    comment = fields.String()
    pms = fields.Nested(PostmachineSchema, many=True)