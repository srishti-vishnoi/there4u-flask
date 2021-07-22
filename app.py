from flask import Flask
from extensions import db, ma
from admin import admin
from modules.user_app import user_blueprint

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key ='1234567890'
db.init_app(app)
ma.init_app(app)
admin.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# Run Server
if __name__ == '__main__':
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.run(debug=True)
