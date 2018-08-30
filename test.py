import sqlite3
def dropTable():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('drop table customer')
    conn.commit()
    conn.close()

def search():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('select * from customer')
    re = cursor.fetchall()
    conn.commit()
    conn.close()
    return re

re = search()
for i in re:
    print(i)