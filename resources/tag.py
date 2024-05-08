from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CategoryModel, TagModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")


@blp.route("/category/<int:category_id>/tag")
class TagsInCategory(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, category_id):
        tag = TagModel(**tag_data, category_id=category_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A tag with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the tag.")
        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagAndItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred linking the tag to the item.")
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred unlinking the tag from the item.")
        return tag


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Deletes a tag if it is not linked to any items.")
    @blp.alt_response(400, description="The tag is linked to an item.")
    @blp.alt_response(404, description="Tag not found.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Tag is linked to an item.")

