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


def createTable():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('''create table likewine (l_id integer primary key AUTOINCREMENT,
    w_id integer not null,
    c_id varchar(30) not null,
    FOREIGN KEY(w_id) REFERENCES wine(w_id), 
    FOREIGN KEY(c_id) references customer(c_id))''')
    conn.close()

createTable()