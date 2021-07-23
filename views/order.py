from model.restaurants import RestaurantItem
from extensions import db
from flask import json, request
from flask_restful import Resource, abort
from services.auth import auth
from model.order import Order as order_model, OrderItem, order_schema, orders_schema, order_item_schema, order_items_schema
from model.user import User as user_model, user_schema
from services.auth import auth

class CreateAndListOrder(Resource):

    @auth.login_required
    def post(self):
        order = order_model(total_amount = 0)
        items = order_items_schema.load(request.json.pop('items'))
        total_amount = 0
        order_items = []
        for item in items:
            res_item = RestaurantItem.query.get(item['restaurant_item_id'])
            if item['quantity'] > res_item.quantity:
                error = {
                    f'{res_item.name}' : f"{res_item.name} is not available with requested quantity"
                }
                abort(400, error = error)
            order_item = OrderItem(
                name=res_item.name,
                price=res_item.price,
                quantity=item['quantity'],
            )
            order_items.append(order_item)
            res_item.quantity -= item['quantity']
            total_amount += order_item.total_price

        user = user_model.query.get(auth.current_user())

        if user.balance < total_amount:
            abort(400, error = "You do not have sufficient balance")
        
        order.total_amount = total_amount
        order.user_id = user.id
        order.restaurant_id = 1
        order.items = order_items
        order.user_id = auth.current_user()
        user.balance -= total_amount
        db.session.add(order)
        db.session.commit()
        return order_schema.dump(order), 200


    @auth.login_required
    def get(self):
        orders = order_model.query.filter_by(user_id = auth.current_user())
        return orders_schema.dump(orders), 200


class Order(Resource):

    @auth.login_required
    def get(self, order_id):
        order = order_model.query.filter_by(id = order_id, user_id = auth.current_user()).first()
        if not order:
            abort(400,message= "Order not found")
        return order_schema.dump(order), 200