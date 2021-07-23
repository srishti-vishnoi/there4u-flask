


from views.user import CreateUser, User, LoginUser, LogoutUser
from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint('user_blueprint', __name__)
api = Api(user_blueprint)


api.add_resource(LoginUser, '/login')
api.add_resource(LogoutUser, '/logout')
api.add_resource(CreateUser, '/')

api.add_resource(User, '/<string:user_id>')
