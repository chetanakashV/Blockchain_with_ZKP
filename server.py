import json
import os
import pickle
from flask import Flask
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from forms import SignupUser,SignIn, ViewReportForm,ViewTransactionForm,AddReportForm,SendReportForm
from flask import Flask, jsonify, request, flash, redirect, url_for, render_template
from config import Config
from blockchain import Blockchain,User,Transaction,Block, userList, b

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)
# if os.path.exists('blockchain.pickle'):
#     with open('blockchain.pickle', 'rb') as f:
#         b= pickle.load(f)
# else:
#     print("Pickle not found")

# if os.path.exists('userList.pickle'):
#     with open('userList.pickle') as f:
#         userList =pickle.load(f)
#         print(userList)
# else:
#     print("The username not found")
#     userList =[]

        
app = Flask(__name__)
app.config.from_object(Config)

login_check=False
login_username=""
password=""


@app.route('/', methods=['GET'])
def base():

    global login_check
    global login_username

    if(not login_check):
        return redirect('/home')

    return render_template('home.html', user=login_username + " (logout)")


@app.route('/home', methods=['GET'])
def home():
    global login_check
    global login_username
    return render_template('home.html',user=login_username + " (logout)")

@app.route('/signup', methods=['GET','POST'])
def signup():
    global login_check
    global login_username
    global password
   
    form=SignupUser(request.form)
    if(request.method =='POST' and form.validate()):
        username =form.username.data
        for user in userList:
            if (user.username == username):
                flash("This username is already taken")
                return redirect("/signup")
        u1 = User(form.username.data,form.password.data)
        userList.append(u1)
        flash("Successfully signed in. You can Login now ",'success')

        return redirect('/login')


    return render_template('signup.html',form=form)


@app.route('/login',methods =['GET','POST'])
def login():
    global login_check
    global login_username
    global password
    
    error = None
    form =SignIn(request.form)
    flag = 0
    if(request.method =='POST' and form.validate()):

        u1 = User(form.username.data,form.password.data)
        for user in userList:
            if (user.username == u1.username and user.password==u1.password):
                login_check=True
                login_username=u1.username
                flag = 1
                flash("Successfully logged in", 'success')
                return redirect('/index')
            else:
                # flash("invalid username or password")
                error = 'Invalid username or password'
        if (flag == 0):
            error = 'Invalid username or password'

    return render_template('login.html',form=form, error = error)

@app.route('/logout', methods=['GET'])
def logout():
    global login_check
    global login_username
    
    login_check = False
    login_username = ''
    return redirect('/login')

# @app.route('/viewreport', methods=['POST', 'GET'])
@app.route('/viewreport', methods=['GET'])
def viewreport():
    global login_check
    global login_username
    global password
    
    
    if(not login_check):
        return redirect('/login')


    error = None
    data = None
    for user in userList:
        if (user.username == login_username):
            data=user.reportList
            print(data)
            if data is None:
                error = "No reports for this user"
    return render_template('viewreport.html', data = data, error = error, user=login_username + " (logout)")


# @app.route('/viewtransaction', methods=['POST', 'GET'])
@app.route('/viewtransaction', methods=['GET'])
def viewtransaction():
    global login_check
    global login_username   
    global password
    
    if(not login_check):
        return redirect('/login')

    transactions = b.viewUser(login_username)
    
    return render_template('viewtransaction.html', data = transactions, user=login_username + " (logout)")


@app.route('/addreport', methods=['POST', 'GET'])
def addreport():

    global login_check   
    global login_username
    global password
    
    if(not login_check):
        return redirect('/login')

    form = AddReportForm(request.form)
   
    if (request.method == 'POST' and form.validate()):
        # user = form.username.data
        report = form.report.data
        for user in userList:
            if (user.username == login_username):
                user.reportList.append(report)
                flash("Report added succesfully",'success')
        return redirect('/index')

    return render_template('addreport.html', form=form, user=login_username + " (logout)")


@app.route('/sendreport', methods=['POST', 'GET'])
def sendreport():

    global login_check    
    global login_username
    global password
    
    error = None
    data = None
    for user in userList:
        if (user.username == login_username):
            data=user.reportList
            print("Reports for user", data)
            if data is None:
                error = "No reports for this user"

    if(not login_check):
        return redirect('/login')

    form = SendReportForm(request.form)
    for user in userList:
            if (user.username == login_username):
                sender = user

    options = [(i, j)  for i,j in enumerate(sender.reportList)]

    # if (request.method == 'POST' and form.validate()):
    if (request.method == 'POST'):
        recipient_un = form.recipient.data
        if recipient_un == login_username:
            flash("Sender and Recipient can't be the same person")
            return redirect('/sendreport')
        
        report = form.report.data
        # report=request.form['report']
        if report is None:
            print("Nothing received")
        print("Report at Backend",report)
        flag = 0
        for user in userList:
            if (user.username == recipient_un):
                recipient = user
                flag = 1
                if(report not in sender.reportList):
                    flash("Report does not exist")
                    return redirect('/sendreport')
                b.addTransaction(Transaction(sender, recipient,report))
                
                flash("Transaction added succesfully",'success')
                return redirect('/index')
        if flag == 0:
            flash("Recipient does not exist")
            return redirect('/sendreport')


    return render_template('sendreport.html', form=form, options = options, data = data, error =error ,user=login_username + " (logout)")

@app.route('/index', methods=['POST', 'GET'])
def index():
    global login_check
    global login_username
    print("Why this is hoppaing",login_username)
    print("SI logged in", login)
    if(not login_check):
        return redirect('/login')
    
    return render_template('index.html', user=login_username + " (logout)")

app.run(debug=True, port=5000)
