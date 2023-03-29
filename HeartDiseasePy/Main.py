from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename

import mysql.connector
import smtplib
# from PIL import Image
import pickle

import numpy as np

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config['DEBUG']


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/UserHome")
def UserHome():
    return render_template('UserHome.html')


@app.route("/NewQuery1")
def NewQuery1():
    return render_template('NewQueryReg.html')


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        n = request.form['name']

        address = request.form['address']
        age = request.form['age']
        pnumber = request.form['phone']
        email = request.form['email']
        zip = request.form['zip']
        uname = request.form['uname']
        password = request.form['psw']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO register VALUES ('','" + n + "','" + age + "','" + email + "','" + pnumber + "','" + zip + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
        return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + username + "' and psw='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            return render_template('index.html')
            return 'Username or Password is wrong'
        else:
            print(data[0])
            session['uid'] = data[0]
            session['mobile'] = data[4]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM register where uname='" + username + "' and psw='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':

        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        aphi = request.form['aphi']
        aplo = request.form['aplo']
        choles = request.form['choles']
        glucose = request.form['glucose']
        smoke = request.form['smoke']
        alcohol = request.form['alcohol']

        slope = request.form['slope']
        ca = request.form['ca']
        thalium = request.form['thalium']

        age = float(age)
        gender = float(gender)
        height = float(height)
        weight = float(weight)
        aphi = float(aphi)
        aplo = float(aplo)
        choles = float(choles)
        glucose = float(glucose)
        smoke = float(smoke)
        alcohol = float(alcohol)
        slope = float(slope)
        ca = float(ca)
        thalium = float(thalium)

        filename = 'static/Model/heart-model.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array([[age, gender, height, weight, aphi, aplo, choles, glucose, smoke, alcohol, slope, ca, thalium]])
        my_prediction = classifier.predict(data)
        Answer =''

        if my_prediction == 1:
            # Answer = 'Heart'

            if (int(thalium) > 4):
                Answer = "Coronary Heart Disease";
                Prescription = "Angiotensin-converting enzyme (ACE) inhibitors "

            elif (int(aphi) > 2):
                Answer = "Cardiac Arrest";

                Prescription = "Coronary bypass surgery ";

            elif (int(aphi) > 3):
                Answer = "High Blood Pressure";
                Prescription = "Beta-blockers ";


            else:
                Answer = "Arrhythmia";
                Prescription = "Procainamide (Procan, Procanbid) ";

            msg = 'Calculations, You have  ' + str(Answer) + 'Prescription : ' + str(Prescription)
            print('Hello:According to our Calculations, You have  Heart Disease')

        else:
            Answer = 'You Do not  have  Heart Disease,your heart is healthy'
            msg = 'Congratulations!!  You Do not have  Heart Disease ,your heart is healthy'
            print('Congratulations!! You Do not have  Heart Disease,your heart is healthy')
            Prescription = 'Nill'

        #sendmsg(session['mobile'],Answer)

        return render_template('Result.html',pre=Answer ,medi=Prescription )



def sendmsg(targetno,message):
    import requests
    requests.post("http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
