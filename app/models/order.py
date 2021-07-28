# /!\ JT w addt'l data AAAAND child in 2 separate O2M relationships
from flask import current_app
from app import db
from datetime import timedelta, datetime 
from .comm_res import CommRes
from app.models import comm_res # importing the class to access the address, which should equal the delivery location here

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, default=datetime.now()) # default is when the button is hit by NPO rep
    delivery_location = db.Column(db.String(200), default=CommRes.delivery_address) # should == the customer's address
    handoff_type = db.Column(db.Boolean, default=False) # False is door drop, True is handed to person

# relationship handling below - add FKs for both rel types --> DOUBLECHECK LOGIC
    # O2M w community resident
    comm_res_id = db.Column(db.Integer, db.ForeignKey('commres.resident_id'))

    # O2M w NPO rep
    npo_rep_id = db.Column(db.Integer, db.ForeignKey('nporep.employee_id'))

    # join table in M2M bw comm_res and offering: remaining FK accounted for
    offering_id = db.Column(db.Integer, db.ForeignKey('offering.offering_id')) # okay for var name to = actual attr name in other model?

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