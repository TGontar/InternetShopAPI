from flask import Flask
from flask_restful import Api
from flask_jwt import *
from security import authenticate, identity
from resources.items import Item, ItemList
from resources.users import UserRegister
from db import db
from create_tables import create_tables
from test import insert_test_values
app = Flask(__name__)
api = Api(app)
db.init_app(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

create_tables()
# with app.app_context():
#     insert_test_values()

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)