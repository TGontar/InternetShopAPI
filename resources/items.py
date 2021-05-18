from flask_restful import reqparse, abort, Resource
from flask_jwt import *
from models.items import Items as ItemModel


def abort_if_item_already_exists(name, message):
    if ItemModel.get(name) !=  None:
        abort(404, message=message)

def abort_if_item_doesnt_exist(name, message):
    if ItemModel.get(name) == None:
        abort(404, message=message)


class Item(Resource):

    @jwt_required()
    def get(self, name):
        abort_if_item_doesnt_exist(name, "Item {} doesn't exist".format(name))
        item = ItemModel.get(name)
        return item.json(), 201

    @jwt_required()
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float)
        args = parser.parse_args()
        abort_if_item_already_exists(name, "Item {} already exist".format(name))
        ItemModel.post(name, args['price'])
        return {"name": name, "price": args['price']}, 201

    @jwt_required()
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float)
        args = parser.parse_args()
        if not ItemModel.get(name):
            ItemModel.post(name, args['price'])
            return {'name': name, 'price': args['price']}, 201
        item = ItemModel.get(name)
        item.price = args['price']
        item.update()
        return args['price'], 201

    @jwt_required()
    def delete(self, name):
        abort_if_item_doesnt_exist(name, "Item {} doesn't exist".format(name))
        ItemModel.delete(name)
        return '', 204


class ItemList(Resource):

    @jwt_required()
    def get(self):
        i = ItemModel.get_all()
        items = []
        for item in i:
            items.append(item.json())
        return items, 201

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=dict, action='append')
        args = parser.parse_args()
        a = []
        for item in args['items']:
            if ItemModel.get(item['name']):
                abort_if_item_already_exists(item['name'], "Item {} already exist".format(item['name']))
            else:
                a.append({'name': item['name'], 'price': item['price']})
                ItemModel.post(item['name'], item['price'])

        return a, 201