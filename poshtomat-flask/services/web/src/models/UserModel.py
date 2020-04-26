from . import db, bcrypt

class UserModel(db.Model):
    __abstract__ = True #check for error if missing
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), unique=True, nullable=False)#auth for both
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, data):
        self.name = data.get('name')
        self.surname = data.get('surname')
        self.phone = data.get('phone')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(value)
            setattr(self, key, item)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):#repl?
        return '<id {}>'.format(self.id)
    