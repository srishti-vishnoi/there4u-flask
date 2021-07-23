


from views.restaurant import Restaurant, AddRestaurantItem, RestaurantItem
from flask import Blueprint
from flask_restful import Api

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__)
api = Api(restaurant_blueprint)


api.add_resource(Restaurant, '/<string:id>')
api.add_resource(AddRestaurantItem, '/<string:res_id>/item')
api.add_resource(RestaurantItem, '/<string:res_id>/item/<string:item_id>/')

