import os
os.system("pip3 install flask")
os.system("pip3 install pyjwt")
os.system("pip3 install pymongo")
os.system("pip install mysql-connector-python")
os.system("pip install python-dotenv")
from flask import Flask, request, jsonify, make_response, request, render_template, session, flash, redirect
import jwt
from pymongo import MongoClient
import mysql.connector
from datetime import datetime, timedelta
from functools import wraps
import time
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'u39u5gh3#RF#*35f#F*#%n3u3f3n59u35f#F#G3'



try:
    MONGO_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Connection to Mongo DB successful")
except:
    print("ERROR CONNECTING TO MONGODB")
    time.sleep(5)
    exit()

try:
    mysql_password = os.getenv("MYSQL_ROOT_PASSWORD")
    mysql_db = os.getenv("MYSQL_DB")
    connection = mysql.connector.connect(
        host="mysql",
        user="root",
        passwd=mysql_password,
        # database=mysql_db
    )
    print("Connection to MySQL DB successful")
except Exception as e:
    print("ERROR CONNECTIONG TO MySQL"+str(e))
    time.sleep(5)
    exit()



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.get('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if not session.get('token'):
            return render_template("login.html")
        else:
            return redirect("/dashboard")
    if request.form['username'] and request.form['password'] == '123456':
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },app.config['SECRET_KEY'])
        session["token"] = token
        res = make_response(redirect("/dashboard"), 200)
        # res.set_cookie('token', token, httponly=True, samesite='Strict')
        return res
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop('token')
    except:
        pass
    return "done" + str(session)


@app.get("/dashboard")
# @token_required
def dashboard():
    cookies = str(session)
    return render_template("dashboard.html", name="sanjiv", data = cookies)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)