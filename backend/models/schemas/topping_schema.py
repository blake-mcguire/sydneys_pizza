from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.toppings import Topping
from models.schemas import ma  

class ToppingReferenceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Topping
        fields = ("topping_id",)
        load_instance = True

class ToppingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Topping
        fields = ("topping_id", "name")
        load_instance = True