from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

from .CourierModel import CourierModel, CourierSchema
from .ClientModel import ClientModel, ClientSchema
from .OrderModel import OrderModel, OrdersSchema
from .PostmachineModel import PostmachineModel, PostmachineSchema