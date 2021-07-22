# id, email(unique), name, city, state, pincode, balance, password, created_at, updated_at,
# first_name, last_name, is_active
from dataclasses import dataclass, field
from sqlalchemy.orm import load_only
from extensions import db, ma
from marshmallow import fields, validate

@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(8))
    balance = db.Column(db.Integer)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)
    is_owner = db.Column(db.Boolean)


    def __init__(self, name, email, password, city, state, zipcode, is_owner = False):
        self.name = name
        self.email = email
        self.balance = 1000
        self.password = password
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.is_owner = is_owner
        self.is_active = True
        [self.first_name, self.last_name] = name.split(" ")

class CreateUserSchema(ma.Schema):
    id= fields.UUID(dump_only=True)
    email = fields.Email()
    name = fields.String(required=True, validate=validate.Length(min=8, max=100))
    first_name  =fields.String(dump_only=True)
    last_name  =fields.String(dump_only=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8, max=200))
    balance= fields.Integer(dump_only=True)
    city = fields.String(required=True, validate=validate.Length(min=3, max=50) )
    state = fields.String(required=True, validate=validate.Length(min=3, max=50) )
    zipcode = fields.String(required=True, validate=validate.Length(min=6, max=8) )
    is_owner = fields.Boolean(load_only= True)

    class Meta:
        model = User

class UserSchema(ma.Schema):
    id= fields.UUID(dump_only=True)
    email = fields.Email()
    name = fields.String(required=True, validate=validate.Length(min=8, max=100))
    first_name  =fields.String(dump_only=True)
    last_name  =fields.String(dump_only=True)
    balance= fields.Integer(dump_only=True)
    city = fields.String(required=True, validate=validate.Length(min=3, max=50) )
    state = fields.String(required=True, validate=validate.Length(min=3, max=50) )
    zipcode = fields.String(required=True, validate=validate.Length(min=6, max=8) )

    class Meta:
        model = User

    


create_user_schema = CreateUserSchema()
user_schema = UserSchema()