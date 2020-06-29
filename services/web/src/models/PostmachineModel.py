from marshmallow import fields, Schema
import datetime
from . import db
from .CellModel import CellSchema, CellModel

class PostmachineModel(db.Model):
    __tablename__ = "post_machines"

    id = db.Column(db.Integer, primary_key=True)
    factory_num = db.Column(db.String(35), unique=True)
    numbox = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(128))
    address = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(128))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    cells = db.relationship(CellModel, backref='cell', lazy=True)

    def __init__(self, data):
        self.factory_num = data.get('factory_num')
        self.numbox = data.get('numbox')
        self.url = data.get('url')
        self.address = data.get('address')
        self.comment = data.get('comment')
        self.place_id = data.get('place_id')
        
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
    def get_all_machines():
        return PostmachineModel.query.all()

    @staticmethod 
    def get_one_machine(id):
        return PostmachineModel.query.get(id)

    @staticmethod
    def get_all_cells_info(id):
        return PostmachineModel.query.get(id)
        


class PostmachineSchema(Schema):
    id = fields.Int(dump_only=True)
    factory_num = fields.String(required=True)
    numbox = fields.Int()
    url = fields.String()
    address = fields.String()
    comment = fields.String()
    place_id = fields.Int()
    cells = fields.Nested(CellSchema, many=True)