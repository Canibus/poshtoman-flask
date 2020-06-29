from marshmallow import fields, Schema
from . import db

class ClientsPlaces(db.Model):
    __tablename__ = "clients_places"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))

    def __init__(self, data):
        self.client_id = data.get('client_id')
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
    def get_all_clients_places():
        return ClientsPlaces.query.all()


class ClientsPlacesSchema(Schema):
    client_id = fields.Int()
    place_id = fields.Int()