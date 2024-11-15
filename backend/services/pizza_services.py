# services/pizza_services.py

from models.pizzas import Pizza
from models.toppings import Topping

def get_all_pizzas(session):
    return session.query(Pizza).all()

def add_pizza(session, name, topping_ids):
    # Retrieve Topping objects based on provided IDs
    toppings = session.query(Topping).filter(Topping.topping_id.in_(topping_ids)).all()
    new_pizza = Pizza(name=name, toppings=toppings)
    session.add(new_pizza)
    session.commit()
    return new_pizza

def update_pizza(session, pizza_id, name, topping_ids):
    pizza = session.query(Pizza).get(pizza_id)
    if pizza:
        pizza.name = name
        toppings = session.query(Topping).filter(Topping.topping_id.in_(topping_ids)).all()
        pizza.toppings = toppings
        session.commit()
    return pizza

def delete_pizza(session, pizza_id):
    pizza = session.query(Pizza).get(pizza_id)
    if pizza:
        session.delete(pizza)
        session.commit()
    return pizza