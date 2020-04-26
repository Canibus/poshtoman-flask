from marshmallow import fields, Schema
import datetime
from . import bcrypt, db
from .CellModel import CellSchema

class PostmachineModel(db.Model):
    __tablename__ = "post_machines"

    id = db.Column(db.Integer, primary_key=True)
    numbox = db.Column(db.Integer, nullable=False)
    #isEmpty = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, data):
        self.numbox = data.get('numbox')

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

class PostmachineSchema(Schema):
    id = fields.Int(dump_only=True)
    numbox = fields.Int()
    cells = fields.Nested(CellSchema, many=True)
    