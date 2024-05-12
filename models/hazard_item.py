from db import db

class HazardItem(db.Model):
    __tablename__ = 'hazard_items'

    hazard_id = db.Column(db.Integer, db.ForeignKey('hazards.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)

    hazard = db.relationship('HazardModel', back_populates='items')
    item = db.relationship('ItemModel', back_populates='hazards')
