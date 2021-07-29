from app import db
from app.models import category 

from app.models.comm_res import CommRes
from app.models.farmer import Farmer
from app.models.npo_rep import NpoRep
from app.models.offering import Offering
from app.models.order import OrderBox
from app.models.farmer_contribution import FarmerContribution
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
farmer_contribution_bp = Blueprint("contributions", __name__,url_prefix="/contributions")
category_bp = Blueprint("produce-categories", __name__, url_prefix="/produce-categories")

# endpoints begin below