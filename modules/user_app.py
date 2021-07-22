from views.user_auth import CreateUser, User
from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint('user_blueprint', __name__)
api = Api(user_blueprint)

api.add_resource(CreateUser, '/')
api.add_resource(User, '/<string:user_id>')
