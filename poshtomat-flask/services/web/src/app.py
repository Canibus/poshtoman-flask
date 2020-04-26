from flask import Flask
from .models import db, bcrypt
from .views.ClientView import client_api as client_blueprint
from .views.CourierView import courier_api as courier_blueprint
from .views.PostmachinesView import pm_api as pm_blueprint
from .views.OrdersView import order_api as order_blueprint
from .views.CellsView import cell_api as cell_blueprint

def create_app():
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object("src.config.Config")

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(client_blueprint, url_prefix='/api/v1/clients')
  app.register_blueprint(courier_blueprint, url_prefix='/api/v1/couriers')
  app.register_blueprint(pm_blueprint, url_prefix='/api/v1/pm')
  app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
  app.register_blueprint(cell_blueprint, url_prefix='/api/v1/cells')

  @app.route('/', methods=['GET'])
  def index():
    return 'Null endpoint'

  return app