from database import db
from sqlalchemy.orm import relationship

class Topping(db.Model):
    __tablename__ = "toppings"
    topping_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Topping {self.topping_id} - {self.name}>"