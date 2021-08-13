from typing import final
from flask.helpers import url_for
import jwt
from werkzeug.utils import redirect
from app import create_app, db
import app

from app.models.offering import OfferingBatch
from app.models.order import OrderBox
from app.models.category import Category
from app.models.user import User ###############
from app.models.offering_order import OfferingOrder ###############

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

from flask_jwt_extended import create_access_token # pip installed flask-jwt-extended in actual project file
from flask_jwt_extended import get_jwt_identity # all taken from docs: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

load_dotenv()

offering_bp = Blueprint("offerings", __name__, url_prefix="/offerings")
order_bp = Blueprint("orders", __name__, url_prefix="/orders")
category_bp = Blueprint("food-categories", __name__, url_prefix="/food-categories")
authorize_bp = Blueprint("auth", __name__, url_prefix="/")
user_bp = Blueprint("users", __name__, url_prefix="/users")
offering_order_bp = Blueprint("offering_orders", __name__, url_prefix="/order-contents") # need?
token_bp = Blueprint("token", __name__, url_prefix="/token") # pba.com/token

# create acct endpoint: take in sign up info; if they hit 'farmer' instantiate that obj, etc; return completed new obj

# create a token w 1hrtut
@token_bp.route("", methods=["GET"]) # pba.com/token;;; was "POST"
def login():
    email = request.json.get("email", None) # was ("username",...)
    password = request.json.get("password", None)

    if email != "test" or password != "test": # when testing the api, use these vals but know that you can change this logic at any time
        return jsonify({"msg": "Bad email or password"}), 401
    access_token = create_access_token(identity=email) # long unhackable value is created by c_a_t func and stored in access_token
    return jsonify(access_token=access_token)


# /!\ DEMO NOTE: see how jwt required decorator prevents web pages from being seen unless the person's logged in!! put dec on real routes
# tut guy used samed bp as login blueprint btw
@token_bp.route("/hello", methods=["GET"]) # pba.com/hello
@jwt_required
def see_hello_inside_app():
    email = get_jwt_identity # the 'Lauren' in 'Hi, Lauren!' when Lauren logs in; works off of line 53!
    for_return = {
        "message": "If you can see this, you're logged in! Welcome, " + email # min 1:12:00 in https://www.youtube.com/watch?v=8-W2O_R95Pk&t=4065s&ab_channel=BreatheCode
    }
    return jsonify(for_return)
        
        
@user_bp.route("", methods=["POST"]) # correct bp?
def create_user():
    """FE logic to hit this endpoint and create a user in BE db"""
    request_body = request.get_json()

    if ("name" not in request_body) and ("email" not in request_body) and ("user_type" not in request_body) and ("username" not in request_body)\
        ("password" not in request_body) and ("address" not in request_body) and ("phone" not in request_body):
        return make_response({"details": "Enter valid data for all fields"}, 400) # msg should be more specific 
    new_user = User.build_user_from_json(request_body)
    db.session.add(new_user)
    db.session.commit()
    return {"user": new_user.json_formatted()}, 201
        
        
        
        
        
        
        # # 11min tut
        # @authorize_bp.route("/register", methods=["GET"])
        # def register_account():
        #     redirect = url_for('auth.auth', _external=True)
        #     return create_app.oauth.google.authorize_redirect(redirect) # was 'oauth_config.oauth.google.authorize_redirect(redirect)'


        # @authorize_bp.route("/authorizeRegister", methods=["GET"]) # check w FE server running
        # def auth_register():
        #     token = create_app.oauth.google.authorize_access_token() # was 'oauth_config.oauth.google....'
        #     user = create_app.oauth.google.parse_id_token(token) # ""

        #     print(user.username) # testing that user's valid; will prob change based on choice to do User tables v commrse/nporep/farmer tables
            
        #     existing_users = db.session.query(User).filter(User.username == user.username).all() # User as in user object, user as in var a couple lines above

        #     if len(existing_users) > 0:
        #         return redirect('/') # parameter!! where should i redirect to?
            
        #     user = User.build_user_from_json()
        #     db.session.add(user)

        #     login_user(user)
        #     return redirect('/app') # parameter!! where should i redirect to?

        # @authorize_bp.route("/auth")
        # def auth():
        #     token = create_app.oauth.google.authorize_access_token() # was 'oauth_config.oauth.google.authorize_access_token()'
        #     user = create_app.oauth.google.parse_id_token(token) # was 'oauth_config.oauth.google.parse_id_token(token)'

        #     existing_users = db.session.query(User).filter(User.username == user.username).all()
        #     if len(existing_users) == 0:
        #         raise "Customer does not exist in the database."
        #     login_user(existing_users[0]) # log in the first queried entry
        #     return redirect('/app') # parameter!! where should i redirect to?

        # # login endpoint:
        #     # take in username and account type + send to different landing pages depending on who they are (FE logic will send to correct page)
        #     # this endpoint confirms that theyre in the db and returns their obj if they are
        # @authorize_bp.route('/login')
        # def login():
        #     oauth = current_app.extensions['authlib.integrations.flask_client']
        #     google = oauth.create_client('google') 
        #     redirect_uri = url_for('authorize', _external=True)
        #     return google.authorize_redirect(redirect_uri) 

        # # logout endpoint
        # @authorize_bp.route("/logout")
        # @login_required
        # def logout():
        #     session.pop('user', None)
        #     logout_user()
        #     return redirect('app') # parameter!! where should i redirect to?


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

# user must be able to view categories
@category_bp.route("", methods=["GET"]) # must be able to create them at '...com/food-categories'
def view_categories():
    """Allow user to see categories"""
    hold_categories = []
    categories = Category.query.all()

    if not categories:
        return jsonify(hold_categories)
    
    for category in categories:
        hold_categories.append(category.json_formatted())
    return jsonify(hold_categories)

# # update/edit a category
# @category_bp.route("/<category_id>", methods=["PUT"]) 
# def update_category(category_id):
#     """Edit a category"""

#     category = Category.query.get(category_id)

#     if not category:
#         return make_response({"details": "No category by that ID"}, 404)
#     request_body = request.get_json()
#     category.category_title = request_body["category_title"]

#     db.session.commit()
#     return {'category': category.json_formatted()}

# # delete a category
# @category_bp.route("/<category_id>", methods=["DELETE"]) 
# def delete_category(category_id):
#     """Delete a category"""

#     category = Category.query.get(category_id)

#     if not category:
#         return make_response({"details": "No category by that ID"}, 404)
#     db.session.delete(category)
#     db.session.commit()
#     return make_response({"details": f"Category '{category.category_title}' deleted."})

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

# user must be able to view offerings (by category only) /// see all herbs offered
@category_bp.route("/<category_id>/offerings", methods=["GET"]) 
def view_offerings():
    """Allow user to see offerings"""
    hold_offerings = []
    offerings = OfferingBatch.query.all()

    if not offerings:
        return jsonify(hold_offerings)
    
    for offering in offerings:
        hold_offerings.append(offering.json_formatted())
    return jsonify(hold_offerings)


# ???? user must be able to view single offerings (by category only) /// click carrot bach # 1 
@category_bp.route("/<category_id>/offerings/<offering_id>", methods=["GET"]) 
def view_single_offering(offering_id):
    """Allow user to see a specific offering batch"""
    offering = OfferingBatch.query.get(offering_id)

    if not offering:
        return make_response({"details": "No offering by that ID."}, 404)
    return {'offering': offering.json_formatted()}, 201 


# update/edit a category
@category_bp.route("/<category_id>", methods=["PUT"]) 
def update_category(category_id):
    """Edit a category"""

    category = Category.query.get(category_id)

    if not category:
        return make_response({"details": "No category by that ID"}, 404)
    
    request_body = request.get_json()
    category.category_title = request_body["category_title"]

    db.session.commit()
    return {'category': category.json_formatted()}

# delete a category
@category_bp.route("/<category_id>", methods=["DELETE"]) 
def delete_category(category_id):
    """Delete a category"""

    category = Category.query.get(category_id)

    if not category:
        return make_response({"details": "No category by that ID"}, 404)
    
    db.session.delete(category)
    db.session.commit()
    return make_response({"details": f"Category '{category.category_title}' deleted."})




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
