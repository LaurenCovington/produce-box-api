from app import db
from app.models import category 

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
category_bp = Blueprint("produce-categories", __name__, url_prefix="/produce-categories")

# /!\ priority 1 routes /!\

# POST ROUTES
# farmer can post offerings BY CATEGORY ONLY - no carrots in the tea section
@category_bp.route("/<category_id>/offerings", methods=["POST"])
def post_offering_by_category(category_id):
    """Allow farmers to post offering batches by category"""

    #relevant_category = Category.query.get(category_id)
    request_body = request.get_json()
    new_offering = OfferingBatch.build_offering_from_json(request_body)

    if not new_offering:
        return make_response({"details": "Invalid data"}, 400)
    if len(new_offering.name) <= 1:
        return make_response({"details": "Please enter valid offering name. Must be greater than 1 character."}, 400)
    if new_offering.total_inventory < 1:
        return make_response({"details": "Must enter at least 1 batch of food."}, 400)
    # if harvest_date format is incorrect, return follow this format YYYY-MM-DD
    
    # tag offering w relevant category id
    new_offering.category_id = category_id
    db.session.commit()
    return {'offering batch': new_offering.json_formatted()}, 201

# commres can create order box
@order_bp.route("", methods=["POST"])
def create_order():
    """Allow community residents to create an order"""
    # this needs to have 'Add to cart' functionality..?








# READ ROUTES
    # commres can see offering categories and offering batches within those categories
    # npo can see all upcoming deliveries (GET all)
    # npo can see the contents, delivery locations, recipient phone # of each order_box for delivery (GET single)
    # npo can see dropoff location where farmer left foods for them to pick up -- does this make sense?
# UPDATE ROUTES
    # commres chooses count of each desired food (think upvote card functionality)
    # commres edits contents of order_box (add, remove) -- add instance methods to one of the models?
# DELETE ROUTES
    # farmer deletes offering batches that are mistakenly posted
    # commres deletes order (more than 24hrs out from drop time)
