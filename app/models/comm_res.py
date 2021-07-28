from flask import current_app
from app import db

class CommRes(db.Model):
    resident_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    delivery_address = db.Column(db.String(200))
    phone = db.Column(db.String(10)) # of 12 char limit for dashes in '111-111-1111'
    donations_sent = db.Column(db.Integer) # reps $ given; may not get to this

# relationship handling below
    # M2M
    orders = db.relationship('Offering', secondary='Order', backref=db.backref('order_placer'), lazy=True) # keep backref names diff?

    # parent in O2M
    expected_deliveries = db.relationship('Order', backref='recipient')

    def json_formatted(self):
        return {
            "id": self.resident_id,
            "name": self.name,
            "delivery_address": self.delivery_address,
            "phone": self.phone,
            "donations_sent": self.donations_sent # may not get to this
        }