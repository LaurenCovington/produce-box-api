# /!\ 
from flask import current_app
from app import db
from datetime import timedelta, datetime 

class Offering(db.Model):
    offering_id = db.Column(db.Integer, primary_key=True)
    offering_type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer) # needs to move to join table bw Offering and Order
    usda_organic = db.Column(db.Boolean, default=False) # flip to true if farmer hits the button
    usage_time_limit = db.Column('in_weeks', db.Integer, nullable=True) # how many weeks a comfrey salve can be used
    side_effects = db.Column(db.String(300), nullable=True) # let herbalists list side effects

# relationship handling below -- dont seem to need any rel handling acc to min 20:25 at https://www.youtube.com/watch?v=OvhoYbjtiKc&t=502s&ab_channel=PrettyPrinted 
    # M2M twice, w farmer
    #contributed = db.relationship('Farmer', secondary='FarmerContributions', backref=db.backref('contributed'), lazy=True)

    # M2M w comm_res
    #menu = db.relationship('CommRes', secondary='FarmerContributions', backref=db.backref('requested'), lazy=True)

    def json_formatted(self):
        return {
            "id": self.offering_id,
            "offering_type": self.offering_type,
            "name": self.name,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory,
            "usda_organic": self.usda_organic,
            "usage_time_limit": self.usage_time_limit,
            "side_effects": self.side_effects
        }

    def update_inventory(self, total_inventory, available_inventory):
        pass
        # every time someone makes an order, adjust the available inventory count to reflect the change

    # /!\ import farmer_contribution to access expiration date and make this func work; func placed here bc nothing expired should make it to the 'box' in f_c
    def remove_expired_foods(self, expiration_date): 
        pass    
        # if today's date == exp_date, adjust available inventory to exclude product(s)

    def toggle_organic(self, usda_organic):
        pass
        # flip default=False to ""=True when farmer hits the button