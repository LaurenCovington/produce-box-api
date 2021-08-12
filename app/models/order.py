# changed
from flask import current_app
from app import db
from datetime import timedelta, datetime 
from .user import User # importing the class to access the address, which should equal the delivery location here

class OrderBox(db.Model):
    __tablename__ = 'order_box' # SM recommended 
    order_id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, default=datetime.now()) # default is when the 'ready to deliver' button is hit by NPO rep
    delivery_location = db.Column(db.String(200), default=User.address) # should == the customer's address
    handoff_type = db.Column(db.Boolean, default=False, nullable=True) # False is door drop, True is handed to person; nullable in case hasnt been delivered yet (is this the only marker of upcoming delivery?)

# relationship handling below 
    #  W User IN PLAY
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
                            # # O2M w community resident
                            # commres_id = db.Column(db.Integer, db.ForeignKey('commres.resident_id'))

                            # # O2M w NPO rep
                            # nporep_id = db.Column(db.Integer, db.ForeignKey('nporep.employee_id'))

    # order needs to contain offerings so that commres can build and npo rep can view them...
    offering_id = db.Column(db.Integer, db.ForeignKey('offering_batch.offering_id')) # how to make sure it holds a list

    def json_formatted(self):
        return {
            "id": self.order_id,
            "delivery_date": self.delivery_date,
            "delivery_location": self.delivery_location,
            "offering_id": self.offering_id,
            "handoff_type": self.handoff_type
        }
    
    @classmethod
    def build_order_from_json(cls, body): # stuff the commres is supposed to enter
        new_order = OrderBox(delivery_location=body['delivery_location'], 
                                    delivery_date=body['delivery_date'],
                                    offering_id=body['offering_id'], # hoping this is a list
                                    handoff_type=body['handoff_type'])
        return new_order