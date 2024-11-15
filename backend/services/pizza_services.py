from sqlalchemy.orm import Session
from sqlalchemy import select
from models.pizzas import Pizza
from models.toppings import Topping

def get_all_pizzas(session: Session):
    return session.execute(select(Pizza)).scalars().all()

def add_pizza(session: Session, name: str, toppings: list):
    new_pizza = Pizza(name=name)
    for topping_id in toppings:
        topping = session.execute(select(Topping).filter(Topping.topping_id == topping_id)).scalar()
        if topping:
            new_pizza.toppings.append(topping)
    session.add(new_pizza)
    session.commit()
    return new_pizza

def update_pizza(session: Session, pizza_id: int, name: str, toppings: list):
    pizza = session.execute(select(Pizza).filter(Pizza.pizza_id == pizza_id)).scalars().first()
    if pizza:
        pizza.name = name
        pizza.toppings.clear()
        for topping_id in toppings:
            topping = session.execute(select(Topping).filter(Topping.topping_id == topping_id)).scalar()
            if topping:
                pizza.toppings.append(topping)
        session.commit()
    return pizza

def delete_pizza(session: Session, pizza_id: int):
    pizza = session.execute(select(Pizza).filter(Pizza.pizza_id == pizza_id)).scalars().first()
    if pizza:
        session.delete(pizza)
        session.commit()
    return pizza