import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

users = [
    (1, 'rolf', 'asdf'),
    (2, 'jose', 'asdf'),
    (3, 'anne', 'xyz')
]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)

connection.commit()
connection.close()
