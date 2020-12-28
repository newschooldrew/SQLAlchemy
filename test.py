import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
# allows us to select things
# responsible for selection of queries and storing result

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)
# runs the query

user = (1,'drew','abc')
insert_query = "INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_query,user)

users = [
    (2,'bob','abc'),
    (3,'anne','abc')
]

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
#saves our changes to the data.db file

connection.close()