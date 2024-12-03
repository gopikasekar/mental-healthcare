from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
import os
import mysql.connector

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1mentaldb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1mentaldb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)
        else:
            flash("UserName or Password Incorrect!")

            return render_template('AdminLogin.html')


@app.route("/Prediction")
def Prediction():
    return render_template('Prediction.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']

        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        Password = request.form['Password']
        City = request.form['City']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1mentaldb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1mentaldb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + age + "','" + mobile + "','" + email + "','" + address + "','" +
                username + "','" + Password + "','" + City + "')")
            conn.commit()
            conn.close()
            return render_template('UserLogin.html')



        else:
            flash('Already Register Username')
            return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['Password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1mentaldb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:

            session['cit'] = data[8]

            return render_template('Prediction.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        import pickle
        import numpy as np
        Answer = ''
        Prescription = ''

        uname = session['uname']
        Gender = request.form['Gender']
        Country = request.form['Country']
        Occupation = request.form['Occupation']
        Self_employed = request.form['Self_employed']
        Family_history = request.form['Family_history']
        Days_indoors = request.form['Days_indoors']

        Growing_stress = request.form['Growing_stress']
        Changes_habits = request.form['Changes_habits']
        Mental_health_history = request.form['Mental_health_history']
        Mood_swings = request.form['Mood_swings']
        Coping_struggles = request.form['Coping_struggles']
        Work_interest = request.form['Work_interest']
        Social_weakness = request.form['Social_weakness']
        Mental_health_interview = request.form['Mental_health_interview']
        Care_options = request.form['Care_options']

        filename2 = 'model.pkl'
        classifier2 = pickle.load(open(filename2, 'rb'))

        data = np.array([[Gender, Country,Occupation, Self_employed, Family_history, Days_indoors,
       Growing_stress, Changes_habits, Mental_health_history,
       Mood_swings, Coping_struggles, Work_interest, Social_weakness,
       Mental_health_interview, Care_options]])
        print(data)
        my_prediction = classifier2.predict(data)
        print(my_prediction[0])

        if my_prediction == 1:

            session['Ans'] = 'Yes'

            Answer = session['uname'] + ' :According to our Calculations, You have  Mental Health Problem'

            Prescription = "mental health conditions may benefit from medications, such as antidepressants, " \
                           "anti-anxiety drugs, mood stabilizers, or antipsychotics. "

        else:
            Answer = session['uname'] + " Congratulations!!  You DON'T have Mental Health Problem "

            Prescription = "Nil"

            session['Ans'] = 'No'

        return render_template('Result.html', result=Answer, fer=Prescription)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
