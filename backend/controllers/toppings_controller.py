from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
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
    with Session(db.engine) as session:
        toppings = get_all_toppings(session)
    return toppings_schema.jsonify(toppings), 200

@toppings_bp.route("/toppings", methods=["POST"])
def add_topping_route():
    try:
        topping_data = topping_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    with Session(db.engine) as session:
        new_topping = add_topping(session, topping_data['name'])
    return topping_schema.jsonify(new_topping), 201

@toppings_bp.route("/toppings/<int:topping_id>", methods=["PUT"])
def edit_topping_route(topping_id):
    try:
        topping_data = topping_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    with Session(db.engine) as session:
        topping = update_topping(session, topping_id, topping_data['name'])
        if not topping:
            return jsonify({"error": "Topping not found"}), 404
    return topping_schema.jsonify(topping), 200

@toppings_bp.route("/toppings/<int:topping_id>", methods=["DELETE"])
def delete_topping_route(topping_id):
    with Session(db.engine) as session:
        topping = delete_topping(session, topping_id)
        if not topping:
            return jsonify({"error": "Topping not found"}), 404
    return jsonify({"message": "Topping removed successfully"}), 200