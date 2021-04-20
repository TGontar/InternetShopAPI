import sqlite3
def insert_test_values():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    create_user = 'INSERT INTO users(id, username, password) VALUES (NULL, ?, ?)'
    user = ('suetolog', '123')

    cursor.execute(create_user, user)
    users = [
        ('dima', 'slave'),
        ('timofey', 'rab')
    ]
    cursor.executemany(create_user, users)


    create_item =  'INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)'
    item = ('milk', 100)
    cursor.execute(create_item, item)

    items = [
        ('bread', 50),
        ('cheese', 200)
    ]
    cursor.executemany(create_item, items)

    connection.commit()
    connection.close()
