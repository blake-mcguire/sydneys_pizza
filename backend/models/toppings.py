from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey

class Topping(Base):
    __tablename__ = "toppings"
    topping_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Topping {self.topping_id} - {self.name}>"