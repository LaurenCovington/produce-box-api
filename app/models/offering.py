from flask import current_app
from app import db
from datetime import timedelta, datetime 

class OfferingBatch(db.Model):
    __tablename__ = 'offering_batch' # SM recommended 
    offering_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    total_inventory = db.Column(db.Integer) # only farmers can affect this
    available_inventory = db.Column(db.Integer, default=total_inventory) # only commres can affect this
    usda_organic = db.Column(db.Boolean, default=False) # flip to true if farmer hits the button
    usage_time_limit = db.Column(db.Integer, nullable=True) # how many weeks a comfrey salve can be used
    side_effects = db.Column(db.String(300), nullable=True) # let herbalists list side effects

    harvest_date = db.Column(db.DateTime) # farmer must enter manually? get rid of and just set exp_date to 'now + 3days'?
    expiration_date = db.Column(db.DateTime, default=harvest_date + timedelta(days=7)) # or >>> exp_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=3))
    bake_date = db.Column(db.DateTime, nullable=True) # for breads 
    dried_date = db.Column(db.DateTime, nullable=True) # for herbs and teas
    make_date = db.Column(db.DateTime, nullable=True) # for herbal meds
    dropoff_location = db.Column(db.String(200))

# relationship handling below 
    # child in O2M w category
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    # child in O2M w farmer
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))

    # child in O2M w order_box (Kaida)
    order_box_id = db.Column(db.Integer, db.ForeignKey('order_box.order_id'))

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