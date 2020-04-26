from marshmallow import fields, Schema
import datetime
from . import bcrypt, db

class CellModel(db.Model):
    __tablename__ = "cells"

    id = db.Column(db.Integer, primary_key=True)
    pm_id = db.Column(db.Integer, db.ForeignKey('post_machines.id'), nullable=False)
    isEmpty = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, data):
        self.isEmpty = data.get('isEmpty')
        self.pm_id = data.get('pm_id')

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
    def get_all_cells():
        return CellModel.query.all()

    @staticmethod
    def get_all_cells_inbox(box):
        return CellModel.query.filter(CellModel.pm_id==box)

    @staticmethod 
    def get_one_cell(id):
        return CellModel.query.get(id)

class CellSchema(Schema):
    id = fields.Int(dump_only=True)
    pm_id = fields.Int()
    isEmpty = fields.Boolean(required=True)
    