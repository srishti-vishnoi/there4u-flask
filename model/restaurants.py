
from model.user import UserSchema
from extensions import db, ma
from marshmallow import fields, validate

class RestaurantItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True)
    price = db.Column(db.Integer, nullable =False)
    quantity = db.Column(db.Integer, nullable =False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
    def __str__(self,name, price, quantity = 1):
        self.name = name
        self.price = price
        self.price = quantity

class RestaurantItemSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    price = fields.Integer(required = True)
    quantity = fields.Integer(required = True)
    restaurant_id = fields.Integer()
    class Meta:
        model = RestaurantItem

restaurant_owner = db.Table(
    'restaurant_owner',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    items = db.relationship('RestaurantItem', backref = 'restaurant', cascade='all,delete')

class RestaurantSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=8, max=100))
    items = fields.List(fields.Nested(RestaurantItemSchema))
    owners = fields.List(fields.Nested(UserSchema(only=('id', 'email'))))
    
    class Meta:
        model = Restaurant



restaurant_schema = RestaurantSchema()
restaurant_item_schema = RestaurantItemSchema()
restaurant_items_schema = RestaurantItemSchema(many=True)
