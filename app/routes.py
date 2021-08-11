from typing import final

from flask.helpers import url_for
from werkzeug.utils import redirect
from app import create_app, db
# from app.models import category # why are these here when they're also below?
# from app.models import offering 

from app.models.comm_res import CommRes
from app.models.farmer import Farmer
from app.models.npo_rep import NpoRep
from app.models.offering import OfferingBatch
from app.models.order import OrderBox
from app.models.category import Category
from app.models.user import User ###############

from flask import request, Blueprint, make_response, jsonify, Flask, current_app  
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc 
import os
from dotenv import load_dotenv
import requests

from flask import session
from authlib.integrations.flask_client import OAuth # had to `pip install authlib` from the venv
from flask_login import login_required, login_user, logout_user 
from flask import url_for, render_template

load_dotenv()

comm_res_bp = Blueprint("community-members", __name__, url_prefix="/community-members")
farmer_bp = Blueprint("farmers", __name__, url_prefix="/farmers")
npo_rep_bp = Blueprint("NPO-reps", __name__, url_prefix="/npo-reps")
offering_bp = Blueprint("offerings", __name__, url_prefix="/offerings")
order_bp = Blueprint("orders", __name__, url_prefix="/orders")
category_bp = Blueprint("food-categories", __name__, url_prefix="/food-categories")
authorize_bp = Blueprint("auth", __name__, url_prefix="/")
user_bp = Blueprint("users", __name__, url_prefix="/users")

# create acct endpoint
    # take in sign up info 
    # if they hit 'farmer' instantiate that obj, etc 
    # return completed new obj

@authorize_bp.route("/register", methods=["GET"])
def register_account():
    redirect = url_for('auth.auth', _external=True)
    return create_app.oauth.google.authorize_redirect(redirect) # was 'oauth_config.oauth.google.authorize_redirect(redirect)'


@authorize_bp.route("/authorizeRegister", methods=["GET"]) # check w FE server running
def auth_register():
    token = create_app.oauth.google.authorize_access_token() # was 'oauth_config.oauth.google....'
    user = create_app.oauth.google.parse_id_token(token) # ""

    print(user.username) # testing that user's valid; will prob change based on choice to do User tables v commrse/nporep/farmer tables
    
    existing_users = db.session.query(User).filter(User.username == user.username).all() # User as in user object, user as in var a couple lines above

    if len(existing_users) > 0:
        return redirect('/') # parameter!! where should i redirect to?
    
    user = User.build_user_from_json()
    db.session.add(user)

    login_user(user)
    return redirect('/app') # parameter!! where should i redirect to?

@authorize_bp.route("/auth")
def auth():
    token = create_app.oauth.google.authorize_access_token() # was 'oauth_config.oauth.google.authorize_access_token()'
    user = create_app.oauth.google.parse_id_token(token) # was 'oauth_config.oauth.google.parse_id_token(token)'

    existing_users = db.session.query(User).filter(User.username == user.username).all()
    if len(existing_users) == 0:
        raise "Customer does not exist in the database."
    login_user(existing_users[0]) # log in the first queried entry
    return redirect('/app') # parameter!! where should i redirect to?

# login endpoint:
    # take in username and account type + send to different landing pages depending on who they are (FE logic will send to correct page)
    # this endpoint confirms that theyre in the db and returns their obj if they are
@authorize_bp.route('/login')
def login():
    oauth = current_app.extensions['authlib.integrations.flask_client']
    google = oauth.create_client('google') 
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri) 

# logout endpoint
@authorize_bp.route("/logout")
@login_required
def logout():
    session.pop('user', None)
    logout_user()
    return redirect('app') # parameter!! where should i redirect to?

















# categories must exist
@category_bp.route("", methods=["POST"]) # must be able to create them at '...com/food-categories'
def create_categories():
    """Allow first user to create relevant categories"""
    request_body = request.get_json()

    if "category_title" not in request_body:
        return make_response({"details": "Enter valid category name"}, 400)
    new_category = Category(category_title=request_body["category_title"])
    
    db.session.add(new_category)
    db.session.commit()
    return {"category": new_category.json_formatted()}, 201

# farmer must post offerings via category
@category_bp.route("/<category_id>/offerings", methods=["POST"]) 
def post_offering_by_category(category_id):
    """Allow farmers to post offering batches by category""" # PROMPT FARMER W FOLLOWING DATE FORMAT ON BUTTON: YYYY-MM-DD; "2021-08-02" in postman >>> Mon, 02 Aug 2021 00:00:00 GMT",

    category_id = int(category_id)
    relevant_category = Category.query.get(category_id)
    hold_offering_ids = [] # unnecesary line..?

    request_body = request.get_json()
    new_offering = OfferingBatch.build_offering_from_json(request_body)
    
    if not new_offering:
        return make_response({"details": "Invalid Data"}, 400)
    if len(new_offering.name) <= 1:
        return make_response({"details": "Enter valid name."}, 400)
    if new_offering.total_inventory < 1:
        return make_response({"details": "Must enter at least 1 batch of food."}, 400)
    db.session.add(new_offering) 

    # link to category
    relevant_category.associated_foods.append(new_offering)
    
    for offering in relevant_category.associated_foods: # unnecesary 'stanza'..?
        hold_offering_ids.append(offering.offering_id)
    db.session.commit()
    return {'offering': new_offering.json_formatted()}, 201 

# customer must be able to create/post an order w contents, delivery address, phone number
@order_bp.route("", methods=["POST"]) # must be created at '...com/orders'
def create_order():
    """Community resident must be able to create an order that holds contents, delivery address and recipient phone number"""
    request_body = request.get_json() # FE logic will hopefully help w populating this request body w the contents correctly
    new_order = OrderBox.build_order_from_json(request_body)

    if not new_order:
        return make_response({"details": "Invalid Data"}, 400)
    if len(new_order.delivery_location) <= 10:
        return make_response({"details": "Enter complete address."}, 400)
    if new_order.offering_id == 0: # correct logic? make sure offering_id is a list of ids like task list
        return make_response({"details": "This order's empty. Choose at least one food."}, 400)
    db.session.add(new_order)
    db.session.commit()
    return {"order": new_order.json_formatted()}, 201

# npo rep must be able to view all orders, sorted by date if possible
@order_bp.route("", methods=["GET"])
def view_orders():
    """NPO rep must be able to view all orders"""
    hold_orders = []
    sorted_orders = request.args.get("sort")

    if not sorted_orders:
        orders = OrderBox.query.all()
    elif sorted_orders == "asc":
        orders = OrderBox.query.order_by(asc(OrderBox.delivery_date)) # make sure asc/desc works on datetime objs
    elif sorted_orders == "desc":
        orders = OrderBox.query.order_by(desc(OrderBox.delivery_date))

    if not orders:
        return jsonify(hold_orders)
    
    for order in orders:
        hold_orders.append(order.json_formatted())
    return jsonify(hold_orders)

# npo rep must be able to confirm order dropoff type for an order: false = door drop, true = in-person exchange
@order_bp.route("/<order_id>/confirm-delivery", methods=["PUT"]) # path? just <order_id>?
def confirm_delivery(order_id):
    """NPO rep must be able to confirm order dropoff type for a single order"""
    order = OrderBox.query.get(order_id)

    if not order:
        return make_response("", 404)
    
    # does this need logic like line 36 in offering.py?
    request_body = request.get_json()
    order.handoff_type = request_body["handoff_type"] # db side reassigned w T or F, user prompted by buttons that say Door Drop (F behind it) and In-Person Hand-Off (T behind it)
    db.session.commit()
    return jsonify({"order": order.json_formatted()})
