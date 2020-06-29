from marshmallow import fields, Schema
from . import db
import datetime


class RentedCellModel(db.Model):
    __tablename__ = "rented_cells"

    id = db.Column(db.Integer, primary_key=True)
    cell_id = db.Column(db.Integer, db.ForeignKey('cells.id'))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    comment = db.Column(db.String(128))
    rentOpen = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    def __init__(self, data):
        self.cell_id = data.get('cell_id')
        self.date_start = datetime.datetime.utcnow()
        self.comment = data.get('isMTC')
        self.rentOpen = 0

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
    def get_all_rented_cells():
        return RentedCellModel.query.all()

    @staticmethod 
    def get_one_rented_cell(id):
        return RentedCellModel.query.get(id)
        


class RentedCellSchema(Schema):
    id = fields.Int(dump_only=True)
    cell_id = fields.Int()
    date_start = fields.DateTime(dump_only=True)
    date_end = fields.DateTime(dump_only=True)
    rentOpen= fields.Int()
    client_id = fields.Int()
    comment = fields.String()