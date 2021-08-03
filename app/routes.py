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
    

    # npo can see all upcoming deliveries (GET all)
    # npo can see the contents, delivery locations, recipient phone # of each order_box for delivery (GET single)
    # npo can see dropoff location where farmer left foods for them to pick up -- does this make sense?
# UPDATE ROUTES
    # commres chooses count of each desired food (think upvote card functionality)
    # commres edits contents of order_box (add, remove) -- add instance methods to one of the models?
# DELETE ROUTES
    # farmer deletes offering batches that are mistakenly posted
    # commres deletes order (more than 24hrs out from drop time)
