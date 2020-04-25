from marshmallow import fields, Schema
import datetime
from . import bcrypt, db

class PostmachineModel(db.Model):
    __tablename__ = "post_machines"

    id = db.Column(db.Integer, primary_key=True)
    isEmpty = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, data):
        self.isEmpty = data.isEmpty

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
    
    @staticmethod
    def get_all_machines():
        return Postmachine.query.all()

    @staticmethod 
    def get_one_machine(id):
        return Postmachine.query.get(id)

class PostmachineSchema(Schema):
    id = fields.Int(dump_only=True)
    isEmpty = fields.Boolean(required=True)
    