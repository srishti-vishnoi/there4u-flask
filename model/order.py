from marshmallow.utils import EXCLUDE, INCLUDE
from sqlalchemy.orm import backref
from extensions import db, ma
from marshmallow import fields, validate
from model.user import UserSchema

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable =False)
    total_price = db.Column(db.Integer, nullable =False)
    quantity = db.Column(db.Integer, nullable =False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    # restaurant_item_id = db.Integer(nullable=False)

    def __init__(self,name, price, quantity = 1):
        self.name = name
        self.price = price
        self.quantity = quantity
        print(price*quantity)
        self.total_price = price * quantity

class OrderItemSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    price = fields.Integer(dump_only = True)
    total_price = fields.Integer(dump_only = True)
    quantity = fields.Integer(required = True)
    order_id = fields.Integer()
    restaurant_item_id = fields.Integer(required = True)

    class Meta:
        model = OrderItem
        unknown = EXCLUDE




class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Integer, nullable =False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order')

    # def __init__(self, total_amount=0):
    #     self.total_amount = total_amount

class OrderSchema(ma.Schema):
      
    id= fields.Integer(dump_only=True)
    total_amount= fields.Integer(nullable=False, validate=validate.Range(1, 100000), dump_only = True)
    items = fields.List(fields.Nested(OrderItemSchema))
    user = fields.Nested(UserSchema(only=('id', 'email',)))
    class Meta:
        model = Order
        unknown = EXCLUDE

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema(many=False)
order_items_schema = OrderItemSchema(many=True)