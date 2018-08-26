import sqlite3
import os
from flask import Flask, render_template,redirect,request,session
from flask_bcrypt import Bcrypt

secret_key = os.urandom(16)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secret_key

# 테이블 생성
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
    conn.close()
createTable()

def searchUser(userId):
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('select * from customer where c_id= ?', [userId])
    cust = cursor.fetchall()
    cust = cust[0]
    conn.close()
    return cust

#메인페이지(임시)
@app.route('/')
def index():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('select * from customer')
    cust = cursor.fetchall()
    conn.close()
    return render_template('index.html',cust=cust)

#유저 회원가입 폼
@app.route('/user/create')
def userCreate():
    return render_template('/user/create.html')

#유저 회원가입 디비 저장
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
    conn.close()
    return redirect('/')

#유저 정보 수정 폼
@app.route('/user/update/<userId>')
def userUpdate(userId):
    cust = searchUser(userId)
    return render_template('/user/update.html',cust=cust)

#유저 정보 수정 디비 반영
@app.route('/user/edit',methods=['POST'])
def userDBupdate():
    data=[request.form['age'],request.form['email'],request.form['address'],request.form['id']]
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('update customer set c_age=?,c_email=?,c_address=? where c_id=?',data)
    conn.commit()
    conn.close()
    return redirect('/')

#유저 정보 삭제
@app.route('/user/delete/<userId>')
def userDBdelete(userId):
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('delete from customer where c_id=?', [userId])
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/user/detail/<userId>')
def userDetail(userId):
    cust = searchUser(userId)
    return render_template('/user/detail.html',cust=cust)

def loginDB(id,pw):
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    try:
        cursor.execute('select c_id,c_pw from customer where c_id=?',[id])
    except Exception as e:
        return False
    else:
        info = cursor.fetchall()
        conn.close()
        info = info[0]
        if info[0] == id:
           return bcrypt.check_password_hash(info[1],pw)
        else:
            return False


#유저 로그인
@app.route('/user/login',methods=['POST'])
def login():
    userId = request.form['id']
    password = request.form['pw']
    try:
        if loginDB(userId , password):
            session['logFlag'] = True
            session['userId'] = userId
            return redirect('/')
        else:
            return '로그인 실패'
    except Exception as e:
        return '로그인 실패 <a href="/">돌아가기</a>'

@app.route('/user/logout')
def logout():
    session['logFlag'] = False
    session.pop('userId', None)
    return redirect('/')

if __name__ == '__main__':
    app.run()
