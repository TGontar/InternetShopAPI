# конструктор пользователей
import sqlite3
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE username = ?'
        row = cur.execute(query, (username, )).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE id = ?'
        row = cur.execute(query, (_id, )).fetchone()

        con.close()

        user = User(*row) if row else None
        return user