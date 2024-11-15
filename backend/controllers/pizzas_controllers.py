from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from database import db
from services.pizza_services import (
    get_all_pizzas, add_pizza, update_pizza, delete_pizza
)
from models.schemas.pizza_schema import PizzaCreateSchema, PizzaRetrieveSchema

pizza_create_schema = PizzaCreateSchema()
pizza_retrieve_schema = PizzaRetrieveSchema(many=True)

pizzas_bp = Blueprint('pizzas', __name__)

@pizzas_bp.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = get_all_pizzas(db.session)
    return pizza_retrieve_schema.jsonify(pizzas), 200

@pizzas_bp.route("/pizzas", methods=["POST"])
def add_pizza_route():
    try:
        # Pass the session to the load method
        pizza_data = pizza_create_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_pizza = add_pizza(db.session, pizza_data['name'], [t['topping_id'] for t in pizza_data['toppings']])
    return pizza_create_schema.jsonify(new_pizza), 201

@pizzas_bp.route("/pizzas/<int:pizza_id>", methods=["PUT"])
def update_pizza_route(pizza_id):
    try:
        # Pass the session to the load method
        pizza_data = pizza_create_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    pizza = update_pizza(db.session, pizza_id, pizza_data['name'], [t['topping_id'] for t in pizza_data['toppings']])
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    db.session.refresh(pizza)
    return pizza_create_schema.jsonify(pizza), 200

@pizzas_bp.route("/pizzas/<int:pizza_id>", methods=["DELETE"])
def delete_pizza_route(pizza_id):
    pizza = delete_pizza(db.session, pizza_id)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    return jsonify({"message": "Pizza removed successfully"}), 200