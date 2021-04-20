from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
import sqlite3

connection = sqlite3.connect('data.db', check_same_thread=False)
cursor = connection.cursor()


parser = reqparse.RequestParser()
parser.add_argument('price')
parser.add_argument('items', type=dict, action="append")

# ошибка если запрашиваемого товара нет
def abort_if_item_doesnt_exist(name):
    if list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)) == []:
        abort(404, message="There's no such item in the shop ({})".format(name))


# ошибка если создаваемый товар уже есть в списке
def abort_if_item_already_exists(name):
    if list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)) != []:
        abort(404, message="You can't add this item, because it already exists ({})".format(name))



class Item(Resource):
    # Получение товара по имени
    @jwt_required()
    def get(self, name):
        abort_if_item_doesnt_exist(name)
        item = list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name))
        return item, 201

    # Создание нового товара по имени
    @jwt_required()
    def post(self, name):
        abort_if_item_already_exists(name)
        args = parser.parse_args()
        query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
        item = (name, args['price'])
        cursor.execute(query, item)
        return "Added items {}".format(item), 201

    # Изменение цены существующего товара по имени, если товара нет - создание нового
    @jwt_required()
    def put(self, name):
        args = parser.parse_args()
        item = (name, args['price'])
        if list(cursor.execute("SELECT * FROM items WHERE name = '%s'" % name)) == []:
            query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
            cursor.execute(query, item)
        else:
            query = "UPDATE items SET price = {0} WHERE name = '{1}'".format(args['price'], name)
            cursor.execute(query)
        return item, 201

    # Удаление товара по имени
    @jwt_required()
    def delete(self, name):
        abort_if_item_doesnt_exist(name)
        query = "DELETE from items WHERE name = '%s'" % name
        cursor.execute(query)
        return '', 204


# Класс списка товаров, где можно посмотреть все товары или добавить сразу несколько их
class ItemList(Resource):

    # Получение списка всех товаров
    @jwt_required()
    def get(self):
        item = list(cursor.execute("SELECT * FROM items"))
        return item, 201

    # Добавление списка сразу нескольких товаров, на вход подается словарь с ключом items
    # и значением - списком из словарей товаров
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        for i in range(len(args['items'])):
            abort_if_item_already_exists(args['items'][i]['name'])
            query = "INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)"
            item = (args['items'][i]['name'], args['items'][i]['price'])
            cursor.execute(query, item)
        return "Successfully added items {}".format(args['items']), 201