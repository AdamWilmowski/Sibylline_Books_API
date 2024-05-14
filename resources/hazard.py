from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import HazardModel
from schemas import HazardSchema

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
