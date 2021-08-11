from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

from auth_decorator import login_required
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth # had to `pip install authlib` from the venv
from flask_login import LoginManager 
import os
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

#@login_required # placed here?
def create_app(test_config=None):
    app = Flask(__name__)

    # Session config
    app.secret_key = os.getenv("APP_SECRET_KEY")
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session' # 
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    # oAuth Setup
    oauth = OAuth(app) # cmd + click gives src code 
    google = oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"), # .env file!
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth', # IG OAuth docs
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/', # IG's 
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'}, # check IG docs for different scope params
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.comm_res import CommRes
    from app.models.farmer import Farmer
    from app.models.npo_rep import NpoRep
    from app.models.offering import OfferingBatch
    from app.models.order import OrderBox
    from app.models.category import Category
    from app.models.user import User

    from .routes import comm_res_bp
    from .routes import farmer_bp
    from .routes import npo_rep_bp
    from .routes import offering_bp
    from .routes import order_bp
    from .routes import category_bp
    from .routes import user_bp

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(comm_res_bp)
    app.register_blueprint(farmer_bp)
    app.register_blueprint(npo_rep_bp)
    app.register_blueprint(offering_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(user_bp)

    return app
