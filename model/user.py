from sqlalchemy.orm import backref
from extensions import db, ma
from marshmallow import fields, validate
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'user'

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

    token = db.relationship('AuthToken', uselist=False, cascade='all,delete')

    restaurants = db.relationship('Restaurant', secondary='restaurant_owner', backref = db.backref('owners', lazy='dynamic'), lazy='joined')

    orders = db.relationship('Order', backref = 'order_owners', cascade='all,delete')

    def __init__(self, name, email, password, city, state, zipcode, is_owner = False):
        self.name = name
        self.email = email
        self.balance = 1000
        self.password = generate_password_hash(password=password)
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.is_owner = is_owner
        self.is_active = True
        [self.first_name, self.last_name] = name.split(" ")

    def __str__(self) -> str:
        return self.name+'::' + self.email

class CreateUserSchema(ma.Schema):
    id= fields.Integer(dump_only=True)
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
    restaurants = fields.List(fields.Nested('RestaurantSchema', only=('id',)))

    class Meta:
        model = User

    


create_user_schema = CreateUserSchema()
user_schema = UserSchema()