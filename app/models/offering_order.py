# Join table to return order contents; associate offering_order_id with and OrderBox obj for displaying contents on the FE
from app.models.offering import OfferingBatch
from flask import current_app
from app import db
from datetime import timedelta, datetime 

class OfferingOrder(db.Model):
    __tablename__ = 'offering_order' # SM recommended 
    contents_id = db.Column(db.Integer, primary_key=True)
    
    # foreign keys
    offering_id = db.Column(db.Integer, db.ForeignKey('offering_batch.offering_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order_box.order_id'))


    def json_formatted(self):
        return {
            "id": self.contents_id,
            "offering_id": self.offering_id,
            "order_id": self.order_id
        }
    
    # is this the logic to call for building an order? like this is what ends up needing to be returned/seen on the UI, right? 
    @classmethod 
    def build_contents_from_json(cls, body): # summary of offerings loaded to an order
        new_collection = OfferingOrder(contents_id=body['contents_id'],
                                        offering_id=body['offering_id'])
        return new_collection

        # ==> [   JT_ID    OF_ID     OR_ID   ]
        # ==> [     1        23        4     ] # what should JT_ID be? OF_ID and OR_ID are correct; reflecting 2 orders, 1 w two items
        # ==> [     2        18        4     ] # redundant (as in change the logic), or misunderstood?
        # ==> [     3        23        12    ]