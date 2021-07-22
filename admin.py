from model.restaurants import Restaurant
from flask_admin import Admin
from model.auth_token import AuthToken
from model.restaurants import Restaurant, RestaurantItem
from model.user import User
from flask_admin.contrib.sqla import ModelView
from extensions import db

admin = Admin()
class UserView(ModelView):
    column_editable_list = ['balance']

admin.add_view(UserView(User, db.session))

admin.add_view(ModelView(Restaurant, db.session))
admin.add_view(ModelView(RestaurantItem, db.session))
