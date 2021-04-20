from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
from items import Item, ItemList
from users import UserRegister
from create_tables import create_tables
from test import insert_test_values
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'

create_tables()
# insert_test_values()

jwt = JWT(app, authenticate, identity)

# парсер запроса


# Эндпоинты
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)