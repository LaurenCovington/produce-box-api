# changed
from flask import current_app
from app import db
from datetime import timedelta, datetime 

class OfferingBatch(db.Model):
    __tablename__ = 'offering_batch' # SM recommended 
    offering_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    total_inventory = db.Column(db.Integer) # only farmers can affect this
    available_inventory = db.Column(db.Integer, default=total_inventory) # only commres can affect this
    usda_organic = db.Column(db.String()) # turning to str bc time; if there's more time later, turn back to 'bool' and flip to true if farmer hits the button
    usage_time_limit = db.Column(db.Integer, nullable=True) # how many weeks a comfrey salve can be used
    side_effects = db.Column(db.String(300), nullable=True) # let herbalists list side effects

    # changed below from harvest_date to contribution date bc formatting convolution + make the exp date work - 8.2.21
    # but its datetime issues arent resolved. null > null, not null > default datetime obj
    contribution_date = db.Column(db.DateTime, default=datetime.now()) # farmer must enter manually w certain format? get rid of and just set exp_date to 'now + 3days'?
    expiration_date = db.Column(db.DateTime, default=contribution_date + timedelta(days=7)) # or >>> exp_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=3))
    bake_date = db.Column(db.DateTime, nullable=True) # for breads, certain format 
    dried_date = db.Column(db.DateTime, nullable=True) # for herbs and teas, certain format
    make_date = db.Column(db.DateTime, nullable=True) # for herbal meds, certain format
    dropoff_location = db.Column(db.String(200)) # selected via drop-down menu on FE

# relationship handling below 
    # child in O2M w category
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    # farmer rel (child in O2M w farmer) in terms of User
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
    
    # child in O2M w farmer
    #farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))

    # child in O2M w order_box (Kaida) //// hold off for now (LJ)
    #order_box_id = db.Column(db.Integer, db.ForeignKey('order_box.order_id'))

    def json_formatted(self):
        if self.usda_organic:
            organic_check = True
        organic_check = False

        return {
            "id": self.offering_id,
            "name": self.name,
            "contribution_date": self.contribution_date,
            "expiration_date": self.expiration_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory,
            "usda_organic": organic_check,
            "bake_date": self.bake_date,
            "dried_date": self.dried_date,
            "make_date": self.make_date,
            "dropoff_location": self.dropoff_location,
            "usage_time_limit": self.usage_time_limit,
            "side_effects": self.side_effects,
            #"category_id": self.category_id,  >> running view_offerings() threw: TypeError: view_offerings() got an unexpected keyword argument 'category_id'
            #"user_id": self.user_id >> ""
        }

    @classmethod
    def build_offering_from_json(cls, body): # stuff the farmer is supposed to enter
        new_offering = OfferingBatch(name=body['name'], 
                                    contribution_date=body['contribution_date'],
                                    expiration_date=body['expiration_date'], # GETTING NULL IN POSTMAN WHEN SHOULD BE GETTING DEFAULT VAL... farmer must enter 'null'/leave field blank and then code will assign default value
                                    total_inventory=body['total_inventory'],
                                    available_inventory=body['total_inventory'], # farmer must enter 'null'/leave field blank and then code will assign default value
                                    usda_organic=body['usda_organic'],
                                    bake_date=body['bake_date'],
                                    dried_date=body['dried_date'],
                                    make_date=body['make_date'],
                                    dropoff_location=body['dropoff_location'],
                                    usage_time_limit=body['usage_time_limit'],
                                    side_effects=body['side_effects'])
        return new_offering

    def update_inventory(self, total_inventory, available_inventory):
        pass
        # every time someone makes an order, adjust the available inventory count to reflect the change

    def remove_expired_foods(self, expiration_date): 
        pass    
        # if today's date == exp_date, adjust available inventory to exclude product(s)

    def toggle_organic(self, usda_organic):
        pass
        # flip default=False to ""=True when farmer hits the button

    def none_left(self):
        pass
    # if total_inv = 0, remove from db