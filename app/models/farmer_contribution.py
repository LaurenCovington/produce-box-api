# /!\ JT w addt'l data
from flask import current_app
from app import db
from datetime import timedelta, datetime 

class FarmerContribution(db.Model):
    __tablename__ = 'farmer_contribution' # SM recommended 
    farm_contr_id = db.Column(db.Integer, primary_key=True)
    harvest_date = db.Column(db.DateTime) # farmer must enter manually? get rid of and just set exp_date to 'now + 3days'?
    #expiration_date = db.Column(db.DateTime, default=datetime.now()) #######
    expiration_date = db.Column(db.DateTime, default=harvest_date + timedelta(days=7)) # or >>> exp_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=3))
    bake_date = db.Column(db.DateTime, nullable=True) # for breads 
    dried_date = db.Column(db.DateTime, nullable=True) # for herbs and teas
    make_date = db.Column(db.DateTime, nullable=True) # for herbal meds
    dropoff_location = db.Column(db.String(200))

# relationship handling below
    # join table in M2M bw farmer and offering, add FKs
    contributing_farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    relevant_offering_id = db.Column(db.Integer, db.ForeignKey('offering.offering_id'))


    def json_formatted(self):
        return {
            "id": self.farm_contr_id,
            "harvest_date": self.harvest_date, # keeping?
            "expiration_date": self.expiration_date, # ""
            "bake_date": self.bake_date,
            "dried_date": self.dried_date,
            "make_date": self.make_date,
            "dropoff_location": self.dropoff_location
        }
