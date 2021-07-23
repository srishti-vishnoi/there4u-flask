# from views.restaurant import Restaurant, AddRestaurantItem, RestaurantItem
from flask import Blueprint
from flask_restful import Api
from views.order import CreateAndListOrder, Order
order_blueprint = Blueprint('order_blueprint', __name__)
api = Api(order_blueprint)


api.add_resource(CreateAndListOrder, '/')
api.add_resource(Order, '/<string:order_id>')
# api.add_resource(RestaurantItem, '/<string:res_id>/item/<string:item_id>/')

