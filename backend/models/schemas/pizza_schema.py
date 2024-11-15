from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class PizzaCreateSchema(ma.Schema):
    pizza_id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    toppings = fields.List(fields.Nested('ToppingReferenceSchema'))

    class Meta:
        fields = ("pizza_id", "name", "toppings")

class PizzaRetrieveSchema(ma.Schema):
    pizza_id = fields.Integer()
    name = fields.String(required=True)
    toppings = fields.List(fields.Nested('ToppingSchema'))

    class Meta:
        fields = ("pizza_id", "name", "toppings")