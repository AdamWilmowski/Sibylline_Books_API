from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="category", lazy="dynamic")
    tags = db.relationship("TagModel", back_populates="category", lazy="dynamic")
