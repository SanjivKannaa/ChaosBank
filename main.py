import os
os.system("pip3 install flask")
os.system("pip3 install pyjwt")
os.system("pip3 install pymongo")
os.system("pip3 install mysql-connector-python")
os.system("pip3 install python-dotenv")
os.system("pip3 install bcrypt")
from flask import Flask, request, jsonify, make_response, request, render_template, session, flash, redirect
import jwt
from pymongo import MongoClient
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from functools import wraps
import time
from dotenv import load_dotenv
load_dotenv()
import bcrypt

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

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
    connection.autocommit=False
    cursor = connection.cursor()
    try:
        cursor.execute("create database "+mysql_db)
    except:
        print("DB already exists")
    try:
        cursor.execute("use "+mysql_db)
        cursor.execute("create table if not exists users (username varchar(20) primary key, password varchar(60) not null, scan_pay_account char(10), normal_pay_account char(10), balance int)")
        cursor.execute("create table if not exists scan_pay_transactions (transaction_number int primary key, date datetime not null, _from char(20) not null, _to char(20) not null, amount int not null)")
        cursor.execute("create table if not exists normal_pay_transactions (transaction_number int primary key, date datetime not null, _from char(20) not null, _to char(20) not null, amount int not null)")
        try:
            cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format("dummy_user", "dummy_password", "0000000001", "0000000001", 0))
        except:
            print("dummy user already exists")
    except Exception as e:
        print(e)
    connection.commit()
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
    login_creds = {
        "username": request.form['username'],
        "password": request.form['password']
    }
    try:
        cursor.execute("select password from users where username=\""+login_creds["username"]+"\"")
        login_creds["hashed_password"] = cursor.fetchall()[0][0]
    except:
        return render_template('login.html', error="User Not Found")
    # return login_creds
    if login_creds["username"]:
        if verify_password(login_creds["password"], login_creds["hashed_password"]): #hash_password(request.form['password']) == login_creds["hashed_password"]:
            token = jwt.encode({
                'username': request.form['username'],
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            },app.config['SECRET_KEY'])
            session["token"] = token
            res = make_response(redirect("/dashboard"), 200)
            # res.set_cookie('token', token, httponly=True, samesite='Strict')
            return res
        else:
            return render_template("login.html", error="Wrong Password")
    else:
        return render_template('login.html', error="User Not Found")


@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop('token')
    except:
        pass
    return redirect("/dashboard")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if not session.get('token'):
            return render_template("register.html")
        else:
            return redirect("/dashboard")
    login_creds = {
        "username": request.form['username'],
        "password": request.form['password'],
        "password2": request.form['password2'],
        "account_type": request.form["account_type"],
        "balance": 0
    }
    if request.form["initial_balance"] != "":
        login_creds["balance"] = int(request.form["initial_balance"])
    if login_creds["password"]!=login_creds["password2"]:
        return render_template("register.html", error='Password mismatch')
    else:
        login_creds["password"] = hash_password(login_creds["password"])
        cursor.execute("select max(scan_pay_account) from users where scan_pay_account <> \"None\"")
        prev_max_scan_pay = cursor.fetchall()
        cursor.execute("select max(normal_pay_account) from users where normal_pay_account <> \"None\"")
        prev_max_normal_pay = cursor.fetchall()
        if prev_max_scan_pay==[[]]:
            prev_max_scan_pay = "00000001"
        else:
            prev_max_scan_pay = str(int(prev_max_scan_pay[0][0]) + 1)
            prev_max_scan_pay = "0"*(10-len(prev_max_scan_pay)) + prev_max_scan_pay
        if prev_max_normal_pay==[[]]:
            prev_max_normal_pay = "00000001"
        else:
            prev_max_normal_pay = str(int(prev_max_normal_pay[0][0]) + 1)
            prev_max_normal_pay = "0"*(10-len(prev_max_normal_pay)) + prev_max_normal_pay
        if login_creds["account_type"] == "scan_pay":
            try:
                cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(login_creds["username"], login_creds["password"], prev_max_scan_pay, None, login_creds["balance"]))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    return render_template("register.html", error="Username already exists")
                elif err.errno == errorcode.ER_DATA_TOO_LONG:
                    return render_template("register.html", error="Too long")
                else:
                    return render_template("register.html", error=str(err))
            connection.commit()
            token = jwt.encode({
                'username': login_creds['username'],
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            },app.config['SECRET_KEY'])
            session["token"] = token
            res = make_response(redirect("/dashboard"), 200)
            # res.set_cookie('token', token, httponly=True, samesite='Strict')
            return res
        elif login_creds["account_type"] == "normal_pay":
            try:
                cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(login_creds["username"], login_creds["password"], None, prev_max_normal_pay, login_creds["balance"]))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    return render_template("register.html", error="Username already exists")
                elif err.errno == errorcode.ER_DATA_TOO_LONG:
                    return render_template("register.html", error="Too long")
                else:
                    return render_template("register.html", error=str(err))
            connection.commit()
            token = jwt.encode({
                'username': login_creds['username'],
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            },app.config['SECRET_KEY'])
            session["token"] = token
            res = make_response(redirect("/dashboard"), 200)
            # res.set_cookie('token', token, httponly=True, samesite='Strict')
            return res
        elif login_creds["account_type"] == "both":
            try:
                cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(login_creds["username"], login_creds["password"], prev_max_scan_pay, prev_max_normal_pay, login_creds["balance"]))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    return render_template("register.html", error="Username already exists")
                elif err.errno == errorcode.ER_DATA_TOO_LONG:
                    return render_template("register.html", error="Too long")
                else:
                    return render_template("register.html", error=str(err))
            connection.commit()
            token = jwt.encode({
                'username': login_creds['username'],
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            },app.config['SECRET_KEY'])
            session["token"] = token
            res = make_response(redirect("/dashboard"), 200)
            # res.set_cookie('token', token, httponly=True, samesite='Strict')
            return res


@app.get("/dashboard")
# @token_required
def dashboard():
    cookies = str(session)
    try:
        token = session["token"]
        username, jwt_exp = str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["username"]), str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["expiration"])
        # if expiration<datetime.now():
        #     return redirect("/logout")
        cursor.execute("select * from users where username=\""+username+"\"")
        data = cursor.fetchone()
        username, scan_pay_account, normal_pay_account, balance = str(data[0]), str(data[2]), str(data[3]), str(data[4])
        return render_template("dashboard.html", username=username, balance=balance, scan_pay_account=scan_pay_account, normal_pay_account=normal_pay_account)
    except Exception as e:
        # return str(e)
        return redirect("/login")


@app.route("/view_transactions", methods=["GET"])
def view_transactions():
    try:
        token = session["token"]
        username, jwt_exp = str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["username"]), str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["expiration"])
        # if expiration<datetime.now():
        #     return redirect("/logout")
        cursor.execute("select scan_pay_account from users where username=\""+username+"\"")
        scan_pay_account_number = cursor.fetchone()[0]
        cursor.execute("select normal_pay_account from users where username=\""+username+"\"")
        normal_pay_account_number = cursor.fetchone()[0]
        cursor.execute("select * from scan_pay_transactions where _from=\""+scan_pay_account_number+"\""+" or _to=\""+scan_pay_account_number+"\" ORDER BY date DESC")
        scan_pay_transactions = cursor.fetchall()
        cursor.execute("select * from normal_pay_transactions where _from=\""+normal_pay_account_number+"\""+" or _to=\""+normal_pay_account_number+"\" ORDER BY date DESC")
        normal_pay_transactions = cursor.fetchall()
        return render_template("view_transactions.html", scan_pay_transactions=scan_pay_transactions, normal_pay_transactions=normal_pay_transactions)
    except Exception as e:
        return redirect("/login")


@app.route("/normal_pay", methods=["GET", "POST"])
def normal_pay():
    try:
        token = session["token"]
        username, jwt_exp = str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["username"]), str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["expiration"])
        # if expiration<datetime.now():
        #     return redirect("/logout")
        if request.method=="GET":
            cursor.execute("select balance from users where username=\""+username+"\"")
            current_balance = cursor.fetchone()[0]
            return render_template("normal_payment.html", sender_account=username, current_balance=current_balance)
        if request.method=="POST":
            try:
                post_data = {
                    "receiver": request.form["receiver"],
                    "amount": int(request.form["amount"])
                }
                cursor.execute("select normal_pay_account from users")
                all_account_numbers = [item for sublist in cursor.fetchall() for item in sublist]
                if post_data["receiver"] not in all_account_numbers:
                    return render_template("transaction_result.html", failure="ERROR: Receiver Not Found")
                cursor.execute("select username from users where normal_pay_account=\""+post_data["receiver"]+"\"")
                receiver_name = cursor.fetchone()[0]
                cursor.execute("select balance from users where username=\""+username+"\"")
                current_balance = cursor.fetchone()[0]
                if post_data["amount"]<=current_balance:
                    # cursor.execute("SET AUTOCOMMIT=0")
                    connection.autocommit=False
                    try:
                        # connection.start_transaction()
                        # actual transaction
                        cursor.execute("select balance from users where normal_pay_account=\""+post_data["receiver"]+"\"")
                        current_balance2 = cursor.fetchone()[0]
                        cursor.execute("update users set balance={} where normal_pay_account=\"{}\"".format(current_balance2+post_data["amount"], post_data["receiver"]))
                        cursor.execute("update users set balance={} where username=\"{}\"".format(current_balance-post_data["amount"], username))
                        cursor.execute("select count(*) from normal_pay_transactions")
                        transaction_number = 1+int(cursor.fetchone()[0])
                        cursor.execute("select normal_pay_account from users where username=\""+username+"\"")
                        sender_account = cursor.fetchone()[0]
                        cursor.execute("insert into normal_pay_transactions values({}, \"{}\", \"{}\", \"{}\", {})".format(transaction_number, str(datetime.now()), sender_account, post_data["receiver"], post_data["amount"]))
                        connection.commit()
                        return render_template("transaction_result.html", amount=post_data["amount"], success=receiver_name, script='''
                        setTimeout(function() {
                            window.location.href = "/dashboard";
                        }, 2000);
                        ''')
                    except Exception as e:
                        connection.rollback()
                        return render_template("transaction_result.html", failure="ERROR: rollback done"+str(e))
                    cursor.execute("SET AUTOCOMMIT=1")
                else:
                    return render_template("transaction_result.html", failure="Insufficient Balance")
            except Exception as e:
                return render_template("transaction_result.html", failure=str(e))
    except:
        return redirect("/login")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)