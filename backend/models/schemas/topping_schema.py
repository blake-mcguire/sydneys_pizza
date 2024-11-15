from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class ToppingReferenceSchema(ma.Schema):
    topping_id = fields.Integer(required=True)

class ToppingSchema(ma.Schema):
    topping_id = fields.Integer()
    name = fields.String(required=True)

    class Meta:
        fields = ("topping_id", "name")