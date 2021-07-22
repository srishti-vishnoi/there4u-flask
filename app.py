# from flask import Flask, g
# from flask_httpauth import HTTPTokenAuth

# app = Flask(__name__)
# auth = HTTPTokenAuth(scheme='Bearer')

# tokens = {
#     "secret-token-1": "john",
#     "secret-token-2": "susan"
# }

# @auth.verify_token
# def verify_token(token):
#     if token in tokens:
#         return tokens[token]

# @app.route('/')
# @auth.login_required
# def index():
#     return "Hello, {}!".format(auth.current_user())

# if __name__ == '__main__':
#     app.run()


from flask import Flask
from extensions import db, ma
from admin import admin
from modules.user_app import user_blueprint

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db.init_app(app)
ma.init_app(app)
admin.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

# Run Server
if __name__ == '__main__':
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.run(debug=True)

