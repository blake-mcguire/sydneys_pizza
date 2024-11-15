from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from database import db
from services.topping_service import (
    get_all_toppings, add_topping, update_topping, delete_topping
)
from models.schemas.topping_schema import ToppingSchema

topping_schema = ToppingSchema()
toppings_schema = ToppingSchema(many=True)

toppings_bp = Blueprint('toppings', __name__)

@toppings_bp.route("/toppings", methods=["GET"])
def get_toppings():
    toppings = get_all_toppings(db.session)
    result = toppings_schema.dump(toppings)
    return jsonify(result), 200

@toppings_bp.route("/toppings", methods=["POST"])
def add_topping_route():
    try:
        # Pass the session to the load method
        topping_data = topping_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_topping = add_topping(db.session, topping_data.name)
    result = topping_schema.dump(new_topping)
    return jsonify(result), 201

@toppings_bp.route("/toppings/<int:topping_id>", methods=["PUT"])
def edit_topping_route(topping_id):
    try:
        topping_data = topping_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    topping = update_topping(db.session, topping_id, topping_data.name)
    if not topping:
        return jsonify({"error": "Topping not found"}), 404
    result = topping_schema.dump(topping)
    return jsonify(result), 200

@toppings_bp.route("/toppings/<int:topping_id>", methods=["DELETE"])
def delete_topping_route(topping_id):
    topping = delete_topping(db.session, topping_id)
    if not topping:
        return jsonify({"error": "Topping not found"}), 404
    return jsonify({"message": "Topping removed successfully"}), 200