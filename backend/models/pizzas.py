from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey

class Pizza(Base):
    __tablename__ = "pizzas"
    pizza_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    toppings: Mapped[list] = relationship('Topping', secondary="pizza_topping", backref="pizzas")

pizza_topping = Table(
    "pizza_topping",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.pizza_id"), primary_key=True),
    Column("topping_id", ForeignKey("toppings.topping_id"), primary_key=True)
)