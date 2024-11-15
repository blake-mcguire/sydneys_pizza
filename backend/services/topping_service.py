# services/topping_service.py
from sqlalchemy import select
from models.toppings import Topping

def get_all_toppings(session):
    return session.execute(select(Topping)).scalars().all()

def add_topping(session, name: str):
    new_topping = Topping(name=name)
    session.add(new_topping)
    session.commit()
    session.refresh(new_topping)  
    return new_topping

def update_topping(session, topping_id: int, name: str):
    topping = session.execute(
        select(Topping).filter(Topping.topping_id == topping_id)
    ).scalars().first()
    if topping:
        topping.name = name
        session.commit()
        session.refresh(topping)  
    return topping

def delete_topping(session, topping_id: int):
    topping = session.execute(
        select(Topping).filter(Topping.topping_id == topping_id)
    ).scalars().first()
    if topping:
        session.delete(topping)
        session.commit()
    return topping