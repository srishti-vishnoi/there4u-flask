from re import I
from sqlite3.dbapi2 import Error
from flask import request
from flask import json
from flask.json import jsonify
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from model.user import User as user_model, create_user_schema, user_schema
from extensions import db
from sqlite3 import IntegrityError


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


class User(Resource):
    def get(self, user_id):
        user = user_model.query.get_or_404(user_id)
        return user_schema.dump(user), 200

    def put(self, user_id):
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

    def delete(self, user_id):
        user = user_model.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
