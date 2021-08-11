from flask import current_app
from app import db

class User(db.Model):
    __tablename__ = 'user' # SM recommended 

    user_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20)) # value would = 'farmer', 'community resident' or 'nporep'

    name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200)) # commres addr, farm addr, or delivery addr depending on user_type
    phone = db.Column(db.String(10)) 
    donations_sent = db.Column(db.Integer, nullable=True) # reps $ given; may not get to this
    donations_received = db.Column(db.Integer) # reps $ given; may not get to this
    contribution_dropoff = db.Column(db.Boolean, default=False, nullable=True) # doesnt count as dropped till farmer hits the button on the phone

    organization = db.Column(db.String(200)) # may not be necessary if the acct's are o-auth'd
    delivery_count = db.Column(db.Integer) # number of deliveries this rep has carried out; need?

    def json_formatted(self):
        return {
            "id": self.user_id,
            "user_type": self.user_type,
            "name": self.name,
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
