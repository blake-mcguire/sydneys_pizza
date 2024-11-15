from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.pizzas import Pizza
from models.toppings import Topping
from models.schemas import ma  # Import the shared Marshmallow instance
from models.schemas.topping_schema import ToppingSchema, ToppingReferenceSchema  # Import ToppingSchema for nested relationships

class PizzaRetrieveSchema(SQLAlchemyAutoSchema):
    toppings = ma.Nested(ToppingSchema, many=True)

    class Meta:
        model = Pizza
        include_fk = True
        include_relationships = True
        load_instance = True

class PizzaCreateSchema(SQLAlchemyAutoSchema):
    toppings = ma.Nested(ToppingReferenceSchema, many=True)

    class Meta:
        model = Pizza
        include_relationships = True
        load_instance = True