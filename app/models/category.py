# not changed
from flask import current_app
from app import db

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_title = db.Column(db.String(100), default="General_Produce") # if farmers don't enter anything, call it general produce

# relationship handling below
    # parent in O2M w offering
    associated_foods = db.relationship('OfferingBatch', backref='assod_category', lazy=True) # was '...backref='category_id')'

    def json_formatted(self):
        return {
            "id": self.category_id, 
            "category_title": self.category_title
        }