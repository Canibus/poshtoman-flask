from marshmallow import fields, Schema
from . import db


class CellModel(db.Model):
    __tablename__ = "cells"

    id = db.Column(db.Integer, primary_key=True)
    isEmpty = db.Column(db.Boolean(), default=True, nullable=False)
    isRent = db.Column(db.Boolean(), default=True, nullable=False)
    isMTC = db.Column(db.Boolean(), default=True, nullable=False)
    pm_id = db.Column(db.Integer, db.ForeignKey('post_machines.id'))
    temp = db.Column(db.Integer)
    comment = db.Column(db.String(128))
    global_open = db.Column(db.Integer)

    def __init__(self, data):
        self.isEmpty = data.get('isEmpty')
        self.isRent = data.get('isRent')
        self.isMTC = data.get('isMTC')
        self.pm_id = data.get('pm_id')
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
    def get_all_cells():
        return CellModel.query.all()

    @staticmethod 
    def get_one_cell(id):
        return CellModel.query.get(id)
        


class CellSchema(Schema):
    id = fields.Int(dump_only=True)
    isEmpty = fields.Boolean()
    isRent = fields.Boolean()
    isMTC = fields.Boolean()
    pm_id = fields.Int()
    temp = fields.Int()
    comment = fields.String()
    global_open = fields.Int()