import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import CategoryModel
from schemas import CategorySchema, PlainCategorySchema
from decorators import require_api_key


blp = Blueprint("Categories", __name__, description="Operations on categories")


@blp.route("/category/<int:category_id>")
class Categories(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}


@blp.route("/category")
class CategoriesList(MethodView):
    @blp.response(201, PlainCategorySchema(many=True))
    def get(self):
        return CategoryModel.query.with_entities(CategoryModel.id, CategoryModel.name).all()

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A category with that name already exists."
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating the category"
            )
        return category
