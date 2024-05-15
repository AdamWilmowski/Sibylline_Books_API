from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    status_points = db.Column(db.Integer, unique=False, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), unique=False, nullable=False)
    category = db.relationship("CategoryModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="item_tags")
    hazards = db.relationship("HazardModel", secondary="hazard_items")
