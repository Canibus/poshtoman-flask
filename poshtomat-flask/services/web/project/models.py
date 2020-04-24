from project import db
import datetime

class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, data):
        self.name = data.get('name')
        self.surname = data.get('surname')
        self.phone = data.get('phone')
        self.email = data.get('email')
        self.password = data.get('password')

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.sesion.commit()
    
class Client(User):
    #miss db.Model inheritence
    __tablename__ = "clients"

    @staticmethod
    def get_all_couriers():
        return Courier.query.all()
    
    @staticmethod 
    def get_one_courier(id):
        return Courier.query.get(id)

class Courier(User):
    #miss db.Model inheritence
    __tablename__ = "couriers"

    @staticmethod
    def get_all_couriers():
        return Courier.query.all()
    
    @staticmethod 
    def get_one_courier(id):
        return Courier.query.get(id)

class Postmachine(db.Model):
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
            setattr(self, name, key)
        db.session.commit()
    
    @staticmethod
    def get_all_machines():
        return Postmachine.query.all()

    @staticmethod 
    def get_one_machine(id):
        return Postmachine.query.get(id)

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    timeUp = db.Column(db.DateTime)
    timeDowm = db.Column(db.DateTime)
    courierId = db.Column(db.Integer, db.ForeignKey('couriers.id'), primary_key=True)
    postMachineId = db.Column(db.Integer, db.ForeignKey('post_machines.id'))
    clientPhone = db.Column(db.String(128), nullable=False)
    orderTime = db.Column(db.DateTime)
    #userid

    def __init__(self, data):
        self.orderTime = datetime.datetime.utcnow()
        self.clientPhone = data.get('clientPhone')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod 
    def get_one_order(id):
        return Order.query.get(id)