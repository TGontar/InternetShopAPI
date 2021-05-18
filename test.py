import sqlite3
from models.items import Items as ItemModel
from models.users import User
def insert_test_values():
        userjson = {"username": "Ivan", "password": "123123"}
        user1 = User(**userjson)
        user1.post()

        name = "bread"
        price = 1200
        ItemModel.post(name, price)

