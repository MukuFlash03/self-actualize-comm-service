from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging


# Create a logger instance for this module using the module's name
logger = logging.getLogger(__name__)


# Initialize SQLAlchemy instance without binding to app
# This allows us to use the db object across multiple modules
# and initialize it later with init_app()
db = SQLAlchemy()

"""Create and configure the Flask app"""
def create_app():
	# Create a new Flask application instance
	app = Flask(__name__)

  	# Get database URL from environment variable with a default fallback
	database_url = os.environ.get('DATABASE_URL')

	if not database_url:
		logger.warning("DATABASE_URL not set! Using SQLite as fallback.")
		database_url = "sqlite:///test.db"

	print(f"Using database URL: {database_url}")

	app.config['SQLALCHEMY_DATABASE_URI'] = database_url
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# db.init_app(app)

	try:
		db.init_app(app)
		with app.app_context():
			# Create tables if they don't exist
			db.create_all()  
		logger.info("Database initialized successfully")
	except Exception as e:
		logger.error(f"Failed to initialize database: {str(e)}")
		raise

	# Register the API Blueprint with no URL prefix
	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix='')
	logger.info("API routes registered")

	return app
