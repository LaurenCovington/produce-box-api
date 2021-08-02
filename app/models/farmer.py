from flask import current_app
from app import db

class Farmer(db.Model):
    __tablename__ = 'farmer' # SM recommended 
    farmer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    farm_location = db.Column(db.String(200))
    phone = db.Column(db.String(10)) # of 12 char limit for dashes in '111-111-1111'
    donations_received = db.Column(db.Integer) # reps $ given; may not get to this
    contribution_dropoff = db.Column(db.Boolean, default=False) # doesnt count as dropped till farmer hits the button on the phone

# relationship handling below
    # O2M
    contributions = db.relationship('offering_batch', backref='contributor') # or backref='farmer_id'

    def json_formatted(self):
        return {
            "id": self.farmer_id,
            "name": self.name,
            "farm_location": self.farm_location,
            "phone": self.phone,
            "donations_received": self.donations_received, # may not get to this
            "contribution_dropoff": self.contribution_dropoff
        }
    
    def dropoff_toggle(self, contribution_dropoff):
        pass
        # flip default False to True once farmer drops contribs to agreed-upon location + hits button
    