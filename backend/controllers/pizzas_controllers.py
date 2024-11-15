from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session
from marshmallow import ValidationError
from models.pizzas import Pizza
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
    with Session(db.engine) as session:
        pizzas = get_all_pizzas(session)
    return pizza_retrieve_schema.jsonify(pizzas), 200

@pizzas_bp.route("/pizzas", methods=["POST"])
def add_pizza_route():
    try:
        pizza_data = pizza_create_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    with Session(db.engine) as session:
        new_pizza = add_pizza(session, pizza_data['name'], [t['topping_id'] for t in pizza_data['toppings']])
    return pizza_create_schema.jsonify(new_pizza), 201

@pizzas_bp.route("/pizzas/<int:pizza_id>", methods=["PUT"])
def update_pizza_route(pizza_id):
    with Session(db.engine) as session:
        pizza = session.execute(select(Pizza).filter(Pizza.pizza_id == pizza_id)).scalars().first()
        if not pizza:
            return jsonify({"error": "Pizza not found"}), 404
        try:
            pizza_data = pizza_create_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        pizza = update_pizza(session, pizza_id, pizza_data['name'], [t['topping_id'] for t in pizza_data['toppings']])
    return pizza_create_schema.jsonify(pizza), 200

@pizzas_bp.route("/pizzas/<int:pizza_id>", methods=["DELETE"])
def delete_pizza_route(pizza_id):
    with Session(db.engine) as session:
        pizza = delete_pizza(session, pizza_id)
        if not pizza:
            return jsonify({"error": "Pizza not found"}), 404
    return jsonify({"message": "Pizza removed successfully"}), 200