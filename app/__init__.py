from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

	db.init_app(app)

	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	return app
  