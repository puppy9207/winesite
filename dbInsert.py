import sqlite3
import csv
import threading

def createTable():
    try:
        conn = sqlite3.connect('wine.db')
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE if not exists wine (
                    w_id integer not null primary key AUTOINCREMENT,
                    w_ko varchar(400) unique ,
                    w_en varchar(400) unique ,
                    w_val varchar(50) ,
                    w_alcohol float(10) ,
                    w_temp varchar(20),
                    w_price integer(15),
                    w_sugar integer (2),
                    w_acid integer (2),
                    w_body integer (2),
                    w_tarnin integer (2)
                )
                ''')
    finally:
        conn.close()

def insertWine(data):
    cursor.execute('INSERT INTO wine(w_ko,w_en,w_val,w_alcohol,w_temp,w_price,w_sugar,w_acid,w_body,w_tarnin) VALUES(?,?,?,?,?,?,?,?,?,?)',data)
    conn.commit()

def dropTable():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('drop table wine')
    conn.commit()
    conn.close()

createTable()
with open('./wine.csv','r',encoding='utf-8-sig') as f:
    lines = f.readlines()
    newLine = []
    for line in lines:
        line = line.replace(',\n',"")
        line = line.split(",")
        newLine.append(line)
# conn = sqlite3.connect('wine.db')
# cursor = conn.cursor()
# for a,val in enumerate(newLine):
#     try:
#         t1 = threading.Thread(target=insertWine(val),args=(val,))
#         t1.start()
#     except Exception:
#         pass
#     print(a)
# conn.close()

conn = sqlite3.connect('wine.db')
cursor = conn.cursor()
cursor.execute('select count(*) from wine where not w_sugar="None" and not w_acid="None" and not w_body="None" and not w_tarnin="None" and not w_price="None"')
wine = cursor.fetchall()

# with open('output.csv','w',encoding='utf-8',newline='') as f:
#     wr = csv.writer(f)
#     for i in wine:
#         wr.writerow(i)
#         print(i)