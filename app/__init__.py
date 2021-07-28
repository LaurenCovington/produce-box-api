from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.comm_res import CommRes ###### class names!
    from app.models.farmer import Farmer
    from app.models.npo_rep import NpoRep
    from app.models.offering import Offering
    from app.models.order import Order

    from .routes import comm_res_bp # NAMES!
    from .routes import farmer_bp
    from .routes import npo_rep_bp
    from .routes import offering_bp
    from .routes import order_bp

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(comm_res_bp) # NAMES! 
    app.register_blueprint(farmer_bp)
    app.register_blueprint(npo_rep_bp)
    app.register_blueprint(offering_bp)
    app.register_blueprint(order_bp)

    return app