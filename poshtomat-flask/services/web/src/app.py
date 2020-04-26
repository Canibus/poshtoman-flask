from flask import Flask
from .models import db, bcrypt
from .views.ClientView import client_api as user_blueprint


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

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/clients')
  #app.register_blueprint(user_blueprint, url_prefix='/api/v1/couriers')
  #app.register_blueprint(user_blueprint, url_prefix='/api/v1/pm')
  #app.register_blueprint(user_blueprint, url_prefix='/api/v1/orders')

  @app.route('/', methods=['GET'])
  def index():
    return 'Null endpoint'

  return app