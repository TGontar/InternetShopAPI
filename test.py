import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)

create_user = 'INSERT INTO users VALUES (?, ?, ?)'
user = (1, 'suetolog', '123')
cursor.execute(create_user, user)

users = [
    (2, 'dima', 'slave'),
    (3, 'timofey', 'rab')
]
cursor.executemany(create_user, users)
connection.commit()
connection.close()
