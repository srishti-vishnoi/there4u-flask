from sqlalchemy.orm import backref
from extensions import db

class AuthToken(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    token = db.Column(db.String())

    def __init__(self, token):
        self.token = token
