# /!\ JT w addt'l data AAAAND child in 2 separate O2M relationships
from flask import current_app
from app import db
from datetime import timedelta, datetime 
from .comm_res import CommRes
from app.models import comm_res # importing the class to access the address, which should equal the delivery location here

class OrderBox(db.Model):
    __tablename__ = 'order_box' # SM recommended 
    order_id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, default=datetime.now()) # default is when the button is hit by NPO rep
    delivery_location = db.Column(db.String(200), default=CommRes.delivery_address) # should == the customer's address
    handoff_type = db.Column(db.Boolean, default=False) # False is door drop, True is handed to person

# relationship handling below 
    # O2M w community resident
    commres_id = db.Column(db.Integer, db.ForeignKey('commres.resident_id'))

    # O2M w NPO rep
    nporep_id = db.Column(db.Integer, db.ForeignKey('nporep.employee_id'))

    def json_formatted(self):
        return {
            "id": self.order_id,
            "delivery_date": self.delivery_date,
            "delivery_location": self.delivery_location,
            "handoff_type": self.handoff_type
        }
    
    def handoff_toggle(self, handoff_type):
        pass
        # default is False/door drop; flip to True if NPOrep hands to customer and hits button
