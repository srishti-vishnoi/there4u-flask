from flask import Flask
from extensions import db, ma
from admin import admin
from modules.user_app import user_blueprint
from modules.restaurant_app import restaurant_blueprint
from modules.order_app import order_blueprint
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
    app.register_blueprint(order_blueprint, url_prefix='/order')

    app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')
    app.run(debug=True)

