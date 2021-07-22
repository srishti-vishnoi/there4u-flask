from model.auth_token import AuthToken
import jwt
from settings import SECRET_KEY
from extensions import db
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(headers):
    return authenticate(headers)

def encode_auth_token(user):
    try:
        payload = {
            'user': {
                'id' : user.id,
                'email' : user.email
            }
        }
        token =  jwt.encode(
            payload,
            SECRET_KEY, 
            algorithm='HS256'
        )
        authToken = AuthToken(token=token)
        authToken.user = user.id
        db.session.add(authToken)
        db.session.commit()
        return token
    
    except Exception as e:
        raise e

def decode_auth_token(token):
    authToken = AuthToken.query.filter_by(token = token).first()
    if authToken:
        return authToken.user

def authenticate(auth_header):
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        user = decode_auth_token(token=auth_token) 
        return user