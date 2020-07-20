from flask import Flask
from flask_cors import CORS
from .models import db, bcrypt
from .views.ClientView import client_api as client_blueprint
from .views.CourierView import courier_api as courier_blueprint
from .views.PostmachinesView import pm_api as pm_blueprint
from .views.OrdersView import order_api as order_blueprint
from .views.PlaceView import place_api as place_blueprint
from .views.AdminView import admin_api as admin_blueprint
from .views.CellView import cell_api as cell_blueprint
from flask_jwt_extended import JWTManager
from .shared import LoggingMiddleware as middleware

def create_app():
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)
  #app.wsgi_app = middleware.LoggerMiddleware(app.wsgi_app)
  app.config.from_object("src.config.Config")

  CORS(app)
  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)
  jwt = JWTManager(app)

  app.register_blueprint(client_blueprint, url_prefix='/api/v2/clients')
  app.register_blueprint(courier_blueprint, url_prefix='/api/v2/couriers')
  app.register_blueprint(pm_blueprint, url_prefix='/api/v2/pm')
  app.register_blueprint(order_blueprint, url_prefix='/api/v2/orders')
  app.register_blueprint(place_blueprint, url_prefix='/api/v2/places')
  app.register_blueprint(admin_blueprint, url_prefix='/api/v2/admins')
  app.register_blueprint(cell_blueprint, url_prefix='/api/v2/cells')


  @app.route('/', methods=['GET'])
  def index():
    return 'Null endpoint'

  return app