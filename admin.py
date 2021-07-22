from flask_admin import Admin
from flask_admin.model.base import BaseModelView
from model.user import User
from flask_admin.contrib.sqla import ModelView
from extensions import db

admin = Admin()
class UserView(ModelView):
    column_editable_list = ['balance']
# admin.add_view(ModelView(User, db.session))

admin.add_view(UserView(User, db.session))