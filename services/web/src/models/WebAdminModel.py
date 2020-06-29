from marshmallow import fields, Schema
from . import db, bcrypt
import datetime 

class WebAdminModel(db.Model):

    __tablename__ = "web_admin"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(128))

    def __init__(self, data):
        self.login = data.get('login')
        self.password = self.__generate_hash(data.get('password'))
        self.comment = data.get('comment')

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
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):#repl?
        return '<id {}>'.format(self.id)
    
    @staticmethod
    def get_admin_by_login(value):
        return WebAdminModel.query.filter_by(login=value).first()

    @staticmethod 
    def get_one_admin(id):
        return WebAdminModel.query.get(id)
    
class WebAdminSchema(Schema):
    id = fields.Int(dump_only=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    comment = fields.Str()