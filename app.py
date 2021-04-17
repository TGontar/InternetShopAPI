from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'


# список товаров
ITEMS = [
    {
        'name': 'milk',
        'price': '100',
    },
    {
        'name': 'bread',
        'price': '50',
    },
    {
        'name': 'cheese',
        'price': '200',
    },
]




jwt = JWT(app, authenticate, identity)


# ошибка если запрашиваемого товара нет
def abort_if_item_doesnt_exist(name):
    if list(filter(lambda x: x['name'] in name, ITEMS)) == []:
        abort(404, message="There's no such item in the shop ({})".format(name))


# ошибка если создаваемый товар уже есть в списке
def abort_if_item_already_exists(name):
    if list(filter(lambda x: x['name'] in name, ITEMS)) != []:
        abort(404, message="You can't add this item, because it already exists ({})".format(name))


# парсер запроса
parser = reqparse.RequestParser()
parser.add_argument('price')
parser.add_argument('items', type=dict, action="append")


# Класс товаров, где можно выполнять действия с товарами по одному (создать, удалить, поменять, просмотреть)
class Item(Resource):

    # Получение товара по имени
    @jwt_required()
    def get(self, name):
        abort_if_item_doesnt_exist(name)
        item = list(filter(lambda x: x['name'] in name, ITEMS))
        return item, 201

    # Создание нового товара по имени
    @jwt_required()
    def post(self, name):
        abort_if_item_already_exists(name)
        args = parser.parse_args()
        ITEMS.append({'name': name, 'price': args['price']})
        return ITEMS[-1], 201

    # Изменение цены существующего товара по имени, если товара нет - создание нового
    @jwt_required()
    def put(self, name):
        args = parser.parse_args()
        item = {'name': name, 'price': args['price']}
        if list(filter(lambda x: x['name'] in name, ITEMS)) == []:
            ITEMS.append({'name': name, 'price': args['price']})
        else:
            ITEMS[ITEMS.index(*list(filter(lambda x: x['name'] in name, ITEMS)))] = item
        return item, 201

    # Удаление товара по имени
    @jwt_required()
    def delete(self, name):
        abort_if_item_doesnt_exist(name)
        del ITEMS[ITEMS.index(*list(filter(lambda x: x['name'] in name, ITEMS)))]
        return '', 204


# Класс списка товаров, где можно посмотреть все товары или добавить сразу несколько их
class ItemList(Resource):

    # Получение списка всех товаров
    @jwt_required()
    def get(self):
        return ITEMS

    # Добавление списка сразу нескольких товаров, на вход подается словарь с ключом items
    # и значением - списком из словарей товаров
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        for i in range(len(args['items'])):
            abort_if_item_already_exists(args['items'][i]['name'])
            ITEMS.append(args['items'][i])
        return "Successfully added items {}".format(args['items']), 201


# Эндпоинты
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')


if __name__ == '__main__':
    app.run(debug=True)