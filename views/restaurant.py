from marshmallow.exceptions import ValidationError
from extensions import db
from flask import request
from flask_restful import Resource, abort
from model.restaurants import restaurant_schema, restaurant_item_schema, Restaurant as restaurant_model, RestaurantItem as restaurant_item_model
from services.auth import auth

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
            abort(401, error = "Unauthorised Access")
       
        try:
            data = restaurant_item_schema.load(request.json)
            item = restaurant_item_model(**data)
            item.restaurant_id = res_id
            db.session.add(item)
            db.session.commit()
            return restaurant_schema.dump(res), 200
            
        except ValidationError as err:
            abort(400, error = err.messages)
        except:
            abort(500, error = "Internal Server Error")


class RestaurantItem(Resource):

    def get(self, res_id, item_id):
        item = restaurant_item_model.query.get_or_404(item_id)
        if str(item.restaurant_id) != res_id:
            abort(404, error = "Not Found")
        return restaurant_item_schema.dump(item), 200

    @auth.login_required
    def delete(self, res_id, item_id):
        res = restaurant_model.query.get_or_404(res_id)
        item = restaurant_item_model.query.get_or_404(item_id)

        if str(item.restaurant_id) != res_id:
            abort(404, error = "Not Found")

        is_res_owner = checkIsOwner(res=res)
        if not is_res_owner:
            abort(401, error = "Unauthorised Access")
        db.session.delete(item)
        db.session.commit()
        return restaurant_schema.dump(res), 200

    @auth.login_required
    def put(self, res_id, item_id):
        res = restaurant_model.query.get_or_404(res_id)
        item = restaurant_item_model.query.get_or_404(item_id)

        if str(item.restaurant_id) != res_id:
            abort(404, error = "Not Found")

        is_res_owner = checkIsOwner(res=res)
        if not is_res_owner:
            abort(401, error = "Unauthorised Access")
        
        item.price = request.json.get('price', item.price) 
        item.quantity = request.json.get('quantity', item.quantity) 
        db.session.commit()
        return restaurant_schema.dump(res), 200
