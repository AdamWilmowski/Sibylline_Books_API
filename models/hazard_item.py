from db import db

class HazardItem(db.Model):
    __tablename__ = 'hazard_items'

    id = db.Column(db.Integer, primary_key=True)
    hazard_id = db.Column(db.Integer, db.ForeignKey('hazards.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)

