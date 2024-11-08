from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logger = logging.getLogger(__name__)

db = SQLAlchemy()

def create_app():
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
			db.create_all()  # Create tables if they don't exist
		logger.info("Database initialized successfully")
	except Exception as e:
		logger.error(f"Failed to initialize database: {str(e)}")
		raise

	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix='')
	logger.info("API routes registered")

	return app
