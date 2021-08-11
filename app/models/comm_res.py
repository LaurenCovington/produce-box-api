# not changed
from flask import current_app
from app import db

class CommRes(db.Model):
    __tablename__ = 'commres' # SM recommended 
    resident_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50)) # actual username
    password = db.Column(db.String(50), nullable=False)
    
    delivery_address = db.Column(db.String(200))
    
    phone = db.Column(db.String(10)) # of 12 char limit for dashes in '111-111-1111'
    donations_sent = db.Column(db.Integer) # reps $ given; may not get to this

    # parent in O2M
    expected_deliveries = db.relationship('OrderBox', backref='recipient') # first arg in relationship() should be CLASS NAME, NOT TABLE NAME (stack overflow)

    def json_formatted(self):
        return {
            "id": self.resident_id,
            "name": self.name,
            "delivery_address": self.delivery_address,
            "phone": self.phone,
            "donations_sent": self.donations_sent # may not get to this
            # add expected_deliveries to return statement?
        }