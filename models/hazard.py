from db import db

class HazardModel(db.Model):
    __tablename__ = "hazards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    severity_level = db.Column(db.Integer, nullable=False)

    items = db.relationship("ItemModel", secondary="hazard_items", back_populates="hazards")