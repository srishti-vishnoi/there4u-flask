from model.auth_token import AuthToken
from flask import request
from flask import json
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from model.user import User as user_model, create_user_schema, user_schema
from extensions import db
from werkzeug.security import check_password_hash
from services.auth import authenticate, encode_auth_token
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth()


class CreateUser(Resource):
    def post(self):
        try:
            res = create_user_schema.load(request.json)
            user = user_model(**res)
            db.session.add(user)
            db.session.commit()
            return create_user_schema.dump(obj=user), 201

        except ValidationError as err:
            return json.dumps(err.messages), 400

        except:
            return {}, 500

@auth.verify_token
def verify_token(headers):
    return authenticate(headers)

class User(Resource):
    @auth.login_required
    def get(self, user_id):
        if str(auth.current_user()) != user_id:
            return {}, 401
        user = user_model.query.get_or_404(user_id)
        return user_schema.dump(user), 200

    @auth.login_required
    def put(self, user_id):
        if auth.current_user()['id'] != user_id:
            return {}, 401

        user = user_model.query.get_or_404(user_id)

        try:
            data = user_schema.load(request.json)
            user = user_model.query.filter_by(id=user_id).update(data)
            db.session.commit()
            return user_schema.dump(user), 200

        except ValidationError as err:
            return json.dumps(err.messages), 400

        except:
            return {}, 500

    @auth.login_required
    def delete(self, user_id):
        if auth.current_user()['id'] != user_id:
            return {}, 401

        user = user_model.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

class LoginUser(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if not email:
            return 'Email is Missing', 400
        if not password:
            return 'Password is Missing', 400
        user = user_model.query.filter_by(email=email).first()
        if not user:
            return "Email doesn't exist", 400

        if not check_password_hash(user.password, password):
            return "Invalid Credentials", 
        
        token  = encode_auth_token(user) 

        return {'token': token},200

class LogoutUser(Resource):

    @auth.login_required
    def get(self):
        authToken = AuthToken.query.filter_by(user = auth.current_user()).first()
        db.session.delete(authToken)
        db.session.commit()
        return {}, 200

        