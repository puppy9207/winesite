import sqlite3
from os import urandom
from flask import Flask, render_template,redirect,request,session
from flask_bcrypt import Bcrypt
import numpy as np
from scipy.spatial import distance

secret_key = urandom(16)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secret_key

# 테이블 생성
def createTable():
    try:
        conn = sqlite3.connect('wine.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE if not exists customer (
            c_id      VARCHAR(30)  NOT NULL primary key,
            c_name    VARCHAR(30)  NOT NULL,
            c_pw      VARCHAR(40)  NOT NULL, 
            c_gender  CHAR(8)      NOT NULL, 
            c_age     INT          NOT NULL, 
            c_email   VARCHAR(60)  NOT NULL unique, 
            c_address VARCHAR(200) NOT NULL 
        )
        ''')
    finally:
        conn.close()
createTable()

def searchUser(userId):
    try:
        conn = sqlite3.connect('wine.db')
        cursor = conn.cursor()
        cursor.execute('select * from customer where c_id= ?', [userId])
        cust = cursor.fetchall()
        cust = cust[0]
    except Exception as e:
        return False
    finally:
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
    return render_template('project1.html',cust=cust)

#유저 회원가입 폼
@app.route('/user/create')
def userCreate():
    return render_template('/user/create.html')

#유저 회원가입 디비 저장
@app.route('/user/new',methods=['POST'])
def userDBinsert():
    try:
        conn = sqlite3.connect('wine.db')
        cursor = conn.cursor()
        password = bcrypt.generate_password_hash(request.form['password'])
        data = [request.form['userid'],request.form['name'],password,request.form['gender'],
                request.form['age'],request.form['email'],request.form['address']
                ]
        cursor.execute('insert into customer values(?,?,?,?,?,?,?)',data)
        conn.commit()
        conn.close()
    except Exception:
        return redirect('오류 <a href="/">돌아가기</a>')
    return redirect('/')

#유저 정보 수정 폼
@app.route('/user/update/<userId>')
def userUpdate(userId):
    cust = searchUser(userId)
    if cust != False:
        return render_template('/user/update.html',cust=cust)
    elif cust == False:
        #여기에 alert창을 띄우는거 넣어야함
        return redirect('/')

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

@app.route('/user/detail',methods=['POST'])
def userDetailWithRecommend():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('''select wine.w_ko, wine.w_en from likewine 
    INNER JOIN wine on likewine.w_id = wine.w_id 
    INNER JOIN customer on likewine.c_id = customer.c_id where customer.c_id=? ''',[session['userId']])
    userWine = cursor.fetchall()
    if session['logFlag'] == True:
            cust = searchUser(session['userId'])
            acid = request.form['acid']
            alcohol = request.form['alcohol']
            density = request.form['density']
            residual_sugar = request.form['residual_sugar']
            total_sulfur_dioxide = request.form['total_sulfur_dioxide']
            check = True
            if acid == '0' and alcohol == '0' and density=='0' and residual_sugar =='0' and total_sulfur_dioxide=='0':
                check = False
            data = np.genfromtxt('centroid.csv', dtype=np.float32, delimiter=',', skip_header=1,
                                 usecols=(5, 6, 7, 8, 9))

            cluster_cnt = 1
            dis = []
            user_list = [int(acid), int(alcohol), int(density), int(residual_sugar), int(total_sulfur_dioxide)]
            cluster_name = ["WhiteRose", "LoveAlcohol", "Sweetie", "Neutral", "BitterBetter"]

            for i in data:
                dst = distance.euclidean(user_list, i)
                dis.append([dst, cluster_cnt])
                cluster_cnt += 1

            dis = sorted(dis)
            cluster = dis[0][1]
            if cluster == 1:  # WhiteRose
                c_data = [3.8169, 2.1505, 3.87, 3.165, 5]
            elif cluster == 2:  # LoveAlcohol
                c_data = [3.582, 4.7025, 3.075, 1.8005, 2.641004981]
            elif cluster == 3:  # Sweetie
                c_data = [3.67155, 2.134, 4.03, 4.0875, 3.555889247]
            elif cluster == 4:  # Neutral
                c_data = [3.65535, 2.7835, 3.47, 1.7845, 3.281204219]
            else:  # BitterBetter
                c_data = [4.5369, 2.998, 3.845, 1.559, 0.970920012]
            print(c_data)
            # nest for best clustering
            if (sum(user_list) <= 10):  # no specific preference
                cluster = 4
                c_data = [3.65535, 2.7835, 3.47, 1.7845, 3.281204219]
            elif (user_list[3] >= 4):  # high sugar
                cluster = 3
                c_data = [3.67155, 2.134, 4.03, 4.0875, 3.555889247]
            elif (user_list[1] >= 4):  # high alcohol
                cluster = 2
                c_data = [3.582, 4.7025, 3.075, 1.8005, 2.641004981]
            elif (user_list[3] == 1):  # low sugar
                cluster = 5
                c_data = [4.5369, 2.998, 3.845, 1.559, 0.970920012]
            elif (user_list[4] >= 4):  # preference for white/rose not red
                cluster = 1
                c_data = [3.8169, 2.1505, 3.87, 3.165, 5]
            print(cluster)
            labels = ["acid", "alcohol", "density", "residual sugar", "total sulfur dioxide"]
            datasets = [
                {
                    "label": cluster_name[cluster - 1],
                    "backgroundColor": "rgba(200,0,0,0.2)",
                    "data": [c_data[0], c_data[1], c_data[2], c_data[3], c_data[4]]
                },
                {
                    "label": 'user',
                    "backgroundColor": "rgba(0,0,200,0.2)",
                    "data": [user_list[0], user_list[1], user_list[2], user_list[3], user_list[4]]
                }
            ]
            return render_template('/user/detail.html',check=check,
                                   cust=cust,
                                   labels=labels,
                                   datasets=datasets,
                                   userWine=userWine,
                                   cluster=cluster_name[cluster-1])
    else:
            return '잘못된 접근입니다. <a href="/">돌아가기</a>'

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
            return '로그인 실패 <a href="/">돌아가기</a>'
    except Exception as e:
        return '로그인 실패 <a href="/">돌아가기</a>'

@app.route('/user/logout')
def logout():
    session['logFlag'] = False
    session.pop('userId', None)
    return redirect('/')

@app.route('/wine/find',methods=['POST'])
def wineFind():
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    query = request.form['query']
    try:
        if session['logFlag'] ==True:
            userId = session['userId']
        else:
            userId = None
    except KeyError:
        userId = None
    cursor.execute('select * from wine where w_ko like ? or w_en like ?',['%'+query+'%','%'+query+'%'])
    wine = cursor.fetchall()
    conn.close()
    return render_template('/wine/find.html',wine=wine,userId=userId)

@app.route('/wine/aboutWine')
def aboutWine():
    return render_template('/wine/aboutWine.html')

@app.route('/wine/likewine',methods=['POST'])
def likeWine():
    w_id = request.form['w_id']
    c_id = request.form['c_id']
    conn = sqlite3.connect('wine.db')
    cursor = conn.cursor()
    cursor.execute('insert into likewine (w_id,c_id) values(?,?) ',[w_id,c_id])
    conn.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run()
