from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import HazardModel, ItemModel
from schemas import HazardSchema, HazardItemSchema

blp = Blueprint("Hazards", __name__, description="Operations on hazards")

@blp.route("/hazard")
class HazardList(MethodView):
    @blp.response(200, HazardSchema(many=True))
    def get(self):
        hazards = HazardModel.query.all()
        return hazards

    @blp.arguments(HazardSchema)
    @blp.response(201, HazardSchema)
    def post(self, hazard_data):
        hazard = HazardModel(**hazard_data)
        try:
            db.session.add(hazard)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A hazard with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the hazard.")
        return hazard

@blp.route("/hazard/<int:hazard_id>")
class Hazard(MethodView):
    @blp.response(200, HazardSchema)
    def get(self, hazard_id):
        hazard = HazardModel.query.get_or_404(hazard_id)
        return hazard

    @blp.arguments(HazardSchema)
    @blp.response(200, HazardSchema)
    def put(self, hazard_data, hazard_id):
        hazard = HazardModel.query.get_or_404(hazard_id)
        if hazard:
            hazard.name = hazard_data["name"]
            hazard.severity_level = hazard_data["severity_level"]
        else:
            hazard = HazardModel(id=hazard_id, **hazard_data)

        db.session.add(hazard)
        db.session.commit()

        return hazard

    def delete(self, hazard_id):
        hazard = HazardModel.query.get_or_404(hazard_id)
        db.session.delete(hazard)
        db.session.commit()
        return {"message": "Hazard deleted."}


@blp.route("/item/<int:item_id>/hazard/<int:hazard_id>")
class LinkHazardsToItem(MethodView):
    @blp.response(201, HazardItemSchema)  # You need to define this schema
    def post(self, item_id, hazard_id):
        item = ItemModel.query.get_or_404(item_id)
        hazard = HazardModel.query.get_or_404(hazard_id)

        item.hazards.append(hazard)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred linking the hazard to the item.")
        return hazard

