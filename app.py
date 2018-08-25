import sqlite3
from flask import Flask, render_template,redirect,request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


def createTable():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE if not exists customer (
        c_id      VARCHAR(30)  NOT NULL primary key,
        c_pw      VARCHAR(40)  NOT NULL, 
        c_gender  CHAR(8)      NOT NULL, 
        c_age     INT          NOT NULL, 
        c_email   VARCHAR(60)  NOT NULL unique, 
        c_address VARCHAR(200) NOT NULL 
    )
    ''')
createTable()

@app.route('/')
def index():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('select * from customer')
    cust = cursor.fetchall()
    return render_template('index.html',cust=cust)

@app.route('/user/create')
def userCreate():
    return render_template('/user/create.html')

@app.route('/user/new',methods=['POST'])
def userDBinsert():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    password = bcrypt.generate_password_hash(request.form['password'])
    data = [request.form['userid'],password,request.form['gender'],
            request.form['age'],request.form['email'],request.form['address']
            ]
    cursor.execute('insert into customer values(?,?,?,?,?,?)',data)
    conn.commit()
    return redirect('/')

@app.route('/user/update')
def userUpdate():

    return render_template('/user/update.html')

@app.route('user/edit')
def userDBupdate():

    return redirect('/')

if __name__ == '__main__':
    app.run()
