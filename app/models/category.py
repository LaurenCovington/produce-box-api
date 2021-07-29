from flask import current_app
from app import db

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_title = db.Column(db.String(100), default="General_Produce") # if farmers don't enter anything, call it general produce

# relationship handling below
    # parent in O2M w offering
    produce_types = db.relationship('offering', backref='category_id')
