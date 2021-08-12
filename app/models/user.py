from flask import current_app
from app import db

class User(db.Model):
    __tablename__ = 'app_user' # SM recommended 

    user_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), nullable=False) # value would = 'farmer', 'community resident' or 'nporep'

    preferred_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False) # commres addr, farm addr, or delivery addr depending on user_type
    phone = db.Column(db.String(10), nullable=False) 
    donations_sent = db.Column(db.Integer, nullable=True) # reps $ given; may not get to this
    donations_received = db.Column(db.Integer, nullable=True) # reps $ given; may not get to this
    contribution_dropoff = db.Column(db.Boolean, default=False, nullable=True) # doesnt count as dropped till farmer hits the button on the phone

    organization = db.Column(db.String(200), nullable=True) # may not be necessary if the acct's are o-auth'd
    delivery_count = db.Column(db.Integer, nullable=True) # number of deliveries this rep has carried out; need?

    # relationship handling 
        # commres parent in O2M w OrderBox
    expected_deliveries = db.relationship('OrderBox', backref='recipient')

        # farmer parent in O2M Offering
    contributions = db.relationship('OfferingBatch', backref='contributor') # or backref='farmer_id'

        # nporep parent in O2M w OrderBox
    deliveries = db.relationship('OrderBox', backref='deliverer')

    def json_formatted(self):
        return {
            "id": self.user_id,
            "user_type": self.user_type,
            "preferred_name": self.preferred_name,
            "username": self.username,
            "phone": self.phone,
            "donations_sent": self.donations_sent, # may not get to this
            "donations_received": self.donations_received,
            "contribution_dropoff": self.contribution_dropoff
            # org
            # del_ct
            # add expected_deliveries to return statement?
        }



    # build db based on what info's relevant
    # database objects
    # db just stores info, bizz layer has ways to read and write and handle data, ui displays
    # db layer - bizz logic layer - ui layer
