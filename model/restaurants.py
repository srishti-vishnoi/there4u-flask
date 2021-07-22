from re import L

from sqlalchemy.ext.declarative import declarative_base
from extensions import db, ma
from marshmallow import fields, validate

# Base = declarative_base()


restaurant_owner = db.Table(
    'restaurant_owner',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class RestaurantSchema(ma.Schema):
    id= fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=8, max=100))

    class Meta:
        model = Restaurant