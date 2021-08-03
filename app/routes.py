from typing import final
from app import db
from app.models import category
from app.models import offering 

from app.models.comm_res import CommRes
from app.models.farmer import Farmer
from app.models.npo_rep import NpoRep
from app.models.offering import OfferingBatch
from app.models.order import OrderBox
from app.models.category import Category

from flask import request, Blueprint, make_response, jsonify, Flask 
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc 
import os
from dotenv import load_dotenv
import requests

load_dotenv()

comm_res_bp = Blueprint("community-members", __name__, url_prefix="/community-members")
farmer_bp = Blueprint("farmers", __name__, url_prefix="/farmers")
npo_rep_bp = Blueprint("NPO-reps", __name__, url_prefix="/npo-reps")
offering_bp = Blueprint("offerings", __name__, url_prefix="/offerings")
order_bp = Blueprint("orders", __name__, url_prefix="/orders")
category_bp = Blueprint("food-categories", __name__, url_prefix="/food-categories")

# /!\ priority 1 routes /!\

# POST ROUTES
# first NPO rep or farmer user has to create the categories for now...to make it so categories reflect regional offerings ;)
@category_bp.route("", methods=["POST"])
def create_categories():
    """First user creates categories"""
    request_body = request.get_json()

    if "category_title" not in request_body:
        return make_response({"details": "Enter valid category name"}, 400)
    new_category = Category(category_title=request_body["category_title"])
    
    db.session.add(new_category)
    db.session.commit()
    return {"category": new_category.json_formatted()}, 201

# farmer can post offerings BY CATEGORY ONLY - no carrots in the tea section
@category_bp.route("/<category_id>/offerings", methods=["POST"]) # any unnecessary lines in this logic that works but technically isnt correct?
def post_offering_by_category(category_id):
    """Allow farmers to post offering batches by category""" # PROMPT FARMER W FOLLOWING DATE FORMAT ON BUTTON: YYYY-MM-DD; "2021-08-02" in postman >>> Mon, 02 Aug 2021 00:00:00 GMT",

    category_id = int(category_id)
    relevant_category = Category.query.get(category_id)
    hold_offering_ids = []

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
    
    for offering in relevant_category.associated_foods:
        hold_offering_ids.append(offering.offering_id)
    db.session.commit()

    return {'offering': new_offering.json_formatted()}, 201 

# /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
# commres can create order box
@order_bp.route("", methods=["POST"])
def create_order():
    """Allow community residents to create an order"""
    # this needs to have 'Add to cart' functionality..?
# /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\

# READ ROUTES
# commres can see offering categories
@category_bp.route("", methods=["GET"])
def get_all_categories():
    """Shows all categories"""
    hold_categories = []
    categories = Category.query.all()
    if not categories:
        return jsonify(hold_categories)

    for category in categories:
        hold_categories.append(category.json_formatted())
    return jsonify((hold_categories))


# commres can see offering batches within those categories (see all by category only, see single offering within category)
    # have UI category button click event feed to this route for viewing offerings via category
@category_bp.route("/<category_id>/offerings", methods=["GET"])
def get_all_offerings(category_id):
    """Shows offerings sorted by category""" # add asc/desc sorting?
    category = Category.query.get(category_id)

    if category is None:
        return make_response({"details": "Invalid ID"}, 404)

    offering_list = []

    try:
        for offering in category.associated_foods: 
            offering = offering.json_formatted()
            offering_list.append(offering)
    except: 
        return make_response({"details": "There are no foods under this category. "})
    return jsonify(offering_list)

# CAN'T CHECK TILL LJ HELPS WITH POST ORDER ROUTE ABOVE
# npo can see all upcoming deliveries: contents (offering id), delivery locations, recipient phone # (via commres id) of each order_box for delivery (GET single)
@order_bp.route("", methods=["GET"])
def get_all_orders():
    """Allow NPO rep to view all orders"""
    orders = OrderBox.query.all()
    order_list = []

    for order in orders:
        recipient = CommRes.query.get(order.commres_id)
        recipient_phone = recipient.phone
        order_contents = OfferingBatch.query.get(order.offering_id)

        # incorrect return: how to connect all asso'd info in final view?
        order_list.append(order.json_formatted())
        order_list.append(recipient_phone)
        order_list.append(order_contents)
    return jsonify(order_list) 

# npo can see farmer-side dropoff location where farmer left foods for them to pick up -- needed?

# UPDATE ROUTES
# commres chooses count of each desired food (think upvote card functionality)
@offering_bp.route("/<offering_id>/choose_count", methods=["PUT"]) # click Produce > click Carrots > on page where you select how many carrots
def choose_food_count(offering_id):
    """Allow community resident to choose how much of each food for their order"""

    selected_offering = OfferingBatch.query.get(offering_id)

    if not selected_offering:
        return make_response({"details": "No food with this ID"}, 404)
    # need if statement: if 'up' button hit, decrease avail_inv x1/click; elif 'down' button hit, increase, else pass
    # does avail_inv need to be the only attr that changes? should desired_count be added to one of the tables (order_box?)
    selected_offering.available_inventory -= 1

    db.session.commit()
    return {'offering': selected_offering.json_formatted()}

# commres edits contents of order_box (add, remove) -- add instance methods to one of the models?
# delete offering from ORDER, not from DATABASE?
# route path right?
@offering_bp.route("/<offering_id>/remove", methods=["PUT"]) # click Produce > click Carrots > on page where you change your mind about carrots and remove them from your 'cart'
def edit_order_contents(offering_id):
    """Allow community resident to delete foods from their order"""
    request_body = request.get_json() # request holds desired updated counts

    offering = OfferingBatch.query.get(offering_id)
    
    if not offering:
        return make_response({"details": "Invalid ID"}, 404)
    # if they hit some UI-side 'remove' button, set the asso'd order id to null, adjust offering avail_inv back to pre-choice count
    if offering.available_inventory != 0: # filler logic...
        offering.order_box_id = None
        offering.available_inventory = offering.total_inventory # correct? how to set to pre-choice count?

    db.session.add(offering) # re-submit edited offering
    db.session.commit()
    return {"details": f"Food with ID #{offering_id} has been deleted from your order."}

# DELETE ROUTES

# farmer deletes offering batches that are mistakenly posted (must delete w/i cateogry)
@category_bp.route("/<category_id>/offerings/<offering_id>", methods=["DELETE"])
def delete_offering(offering_id):
    """Allow farmer to delete offering batch that is mistakenly posted"""
    offering = OfferingBatch.query.get(offering_id)
    if offering is None:
        return make_response({"details": "No food logged with that ID"}, 404)

    db.session.delete(offering)
    db.session.commit()
    return {"details": f"Offering batch with ID #{offering_id} has been deleted from the database."}

# commres deletes order (more than 24hrs out from drop time)
# cant test till LJ fix
@order_bp.route("/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Allow community resident to delete entire order if they've changed their mind"""
    order = OrderBox.query.get(order_id)
    if order is None:
        return make_response({"details": "No order with that ID"}, 404)

    db.session.delete(order)
    db.session.commit()
    return {"details": f"Order with ID #{order_id} has been deleted. No delivery this week!"}
