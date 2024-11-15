from database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey

pizza_topping = Table(
    "pizza_topping",
    db.Model.metadata,
    Column("pizza_id", ForeignKey("pizzas.pizza_id"), primary_key=True),
    Column("topping_id", ForeignKey("toppings.topping_id"), primary_key=True)
)

class Pizza(db.Model):
    __tablename__ = "pizzas"
    pizza_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    toppings = relationship('Topping', secondary=pizza_topping, backref='pizzas')

    def __repr__(self):
        return f"<Pizza {self.pizza_id} - {self.name}>"