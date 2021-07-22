from marshmallow.exceptions import ValidationError
from extensions import db
from flask import json, request
from flask_restful import Resource
from model.restaurants import restaurant_owner, restaurant_schema, restaurant_item_schema, Restaurant as restaurant_model, RestaurantItem as restaurant_item_model
from services.auth import auth
from model.user import User as user_model, user_schema

def checkIsOwner(res):
        if not auth.current_user():
            return False
        for owner in res.owners:
            if owner.id == auth.current_user():
                return True
        return False

class Restaurant(Resource):
    def get(self, id):
        res = restaurant_model.query.get_or_404(id)
        return restaurant_schema.dump(res), 200


class AddRestaurantItem(Resource):
    
    @auth.login_required
    def post(self, res_id):
        res = restaurant_model.query.get_or_404(res_id)
        is_res_owner = checkIsOwner(res=res)
        if not is_res_owner:
            return {}, 401
       
        try:
            data = restaurant_item_schema.load(request.json)
            item = restaurant_item_model(**data)
            item.restaurant_id = res_id
            db.session.add(item)
            db.session.commit()
            return restaurant_schema.dump(res), 200
            
        except ValidationError as err:
            return json.dumps(err.messages), 400
        except:
            return {}, 500


class RestaurantItem(Resource):

    def get(self, res_id, item_id):
        item = restaurant_item_model.query.get_or_404(item_id)
        if str(item.restaurant_id) != res_id:
            return {}, 400
        return restaurant_item_schema.dump(item), 200

    @auth.login_required
    def delete(self, res_id, item_id):
        res = restaurant_model.query.get_or_404(res_id)
        item = restaurant_item_model.query.get_or_404(item_id)

        if str(item.restaurant_id) != res_id:
            return {}, 400

        is_res_owner = checkIsOwner(res=res)
        if not is_res_owner:
            return {}, 401
        db.session.delete(item)
        db.session.commit()
        return restaurant_schema.dump(res), 200

    @auth.login_required
    def put(self, res_id, item_id):
        print("hiiiiiiiiiii")
        res = restaurant_model.query.get_or_404(res_id)
        item = restaurant_item_model.query.get_or_404(item_id)

        if str(item.restaurant_id) != res_id:
            return {}, 400

        is_res_owner = checkIsOwner(res=res)
        if not is_res_owner:
            return {}, 401
        
        item.price = request.json.get('price', item.price) 
        item.quantity = request.json.get('quantity', item.quantity) 
        db.session.commit()
        return restaurant_schema.dump(res), 200
