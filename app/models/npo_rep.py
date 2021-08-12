# # not changed
# from flask import current_app
# from app import db

# class NpoRep(db.Model):
#     __tablename__ = 'nporep' # SM recommended 
#     employee_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     username = db.Column(db.String(50)) # actual username
#     password = db.Column(db.String(50), nullable=False)
#     organization = db.Column(db.String(200))
#     phone = db.Column(db.String(10)) # of 12 char limit for dashes in '111-111-1111'
#     delivery_count = db.Column(db.Integer) # number of deliveries this rep has carried out

# # relationship handling below
#     # parent in O2M
#     deliveries = db.relationship('OrderBox', backref='deliverer')

#     def json_formatted(self):
#         return {
#             "id": self.employee_id,
#             "name": self.name,
#             "organization": self.organization,
#             "phone": self.phone,
#             "delivery_count": self.delivery_count # may not get to this
#         }

#     def count_deliveries(self, delivery_count):
#         pass
#         # up the count everytime rep marks that they delivered (in hand or door drop)