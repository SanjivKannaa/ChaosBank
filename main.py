import os
# os.system("pip3 install flask")
# os.system("pip3 install pyjwt")
# os.system("pip3 install pymongo")
# os.system("pip3 install mysql-connector-python")
# os.system("pip3 install python-dotenv")
# os.system("pip3 install bcrypt")
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
app.config['SECRET_KEY'] = os.getenv("JWT_SECRET")



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
        cursor.execute("create table if not exists users (username varchar(20) unique not null, password varchar(60) not null, account_number char(10) primary key not null, balance int not null)")
        cursor.execute("create table if not exists transactions (transaction_number int primary key not null, date datetime not null, _from char(20) not null, _to char(20) not null, amount int not null, FOREIGN KEY (_from) REFERENCES users(account_number),FOREIGN KEY (_to) REFERENCES users(account_number))")
        try:
            cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\")".format("dummy_user", "dummy_password", "0000000001", 0))
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
    return make_response({
        "message": "ReliaBank API is working",
        "for documentation": "visit /docs"
    }, 200)

@app.route('/docs', methods=["GET"])
def docs():
    return make_response({
        "/": {
            "info": "health check endpoint",
            "request type": "GET"
        },
        "/docs": {
            "info": "view this documentation",
            "request type": "GET"
        },
        "/register": {
            "info": "register as a new user",
            "request type": "POST",
            "payload": {
                "username": "your_username",
                "password": "your_password",
                "balance": "your_initial_balance"
            }
        },
        "/login": {
            "info": "login as an existing user",
            "request type": "POST",
            "payload": {
                "username": "your_username",
                "password": "your_password"
            }
        },
        "/logout": {
            "info": "logout",
            "request type": "GET"
        },
        "/dashboard": {
            "info": "get stats for your account",
            "request type": "GET"
        },
        "/view_transactions": {
            "info": "view all transaction of the current user",
            "request type": "GET"
        },
        "/transfer": {
            "info": "transfer money to another account",
            "request type": "POST",
            "payload": {
                "receiver": "receiver account number",
                "amount": "amount"
            }
        }
    }, 200)

@app.route('/login', methods=['POST'])
def login():
    try:
        req_body = request.json
        login_creds = {
            "username": req_body['username'],
            "password": req_body['password']
        }
    except:
        return make_response({
            "message": "login failed",
            "error": "not all required parameters are passed",
            "code": "0"
        }, 404)
    try:
        cursor.execute("select password from users where username=\""+login_creds["username"]+"\"")
        login_creds["hashed_password"] = cursor.fetchall()[0][0]
    except:
        return make_response({
            "message": "login failed",
            "error": "User Not Found",
            "code": "0"
        }, 400)
    # return login_creds
    if login_creds["username"]:
        if verify_password(login_creds["password"], login_creds["hashed_password"]): #hash_password(request.form['password']) == login_creds["hashed_password"]:
            token = jwt.encode({
                'username': login_creds['username'],
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            },app.config['SECRET_KEY'])
            session["token"] = token
            return make_response({
                "message": "login success",
                "error": "",
                "code": "1"
            }, 200)
        else:
            return make_response({
                "message": "login failed",
                "error": "Wrong Password",
                "code": "0"
            }, 400)
    else:
        return make_response({
            "message": "login failed",
            "error": "User Not Found",
            "code": "0"
        }, 400)


@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop('token')
    except:
        pass
    return make_response({
        "message": "logout success",
        "error": "",
        "code": "1"
    }, 200)


@app.route('/register', methods=['POST'])
def register():
    try:
        req_body = request.json
        login_creds = {
            "username": req_body['username'],
            "password": req_body['password'],
            "balance": 0
        }
    except:
        return make_response({
            "message": "registration failed",
            "error": "all required parameters arent passed",
            "code": "0"
        }, 400)
    try:
        login_creds["balance"] = int(req_body["balance"])
    except:
        return make_response({
            "message": "registration failed",
            "error": "\"balance\" needs to be an integer",
            "code": "0"
        }, 400)
    login_creds["password"] = hash_password(login_creds["password"])
    cursor.execute("select max(account_number) from users where account_number <> \"None\"")
    account_number = cursor.fetchall()
    if account_number==[[]]:
        account_number = "00000001"
    else:
        account_number = str(int(account_number[0][0]) + 1)
        account_number = "0"*(10-len(account_number)) + account_number
    try:
        cursor.execute("insert into users values (\"{}\", \"{}\", \"{}\", \"{}\")".format(login_creds["username"], login_creds["password"], account_number, login_creds["balance"]))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            return make_response({
                "message": "registration failed",
                "error": "username already used",
                "code": "0"
            }, 400)
        elif err.errno == errorcode.ER_DATA_TOO_LONG:
            return make_response({
                "message": "registration failed",
                "error": "data too long",
                "code": "0"
            }, 400)
        else:
            return make_response({
                "message": "registration failed",
                "error": str(e),
                "code": "0"
            }, 400)
    connection.commit()
    token = jwt.encode({
        'username': login_creds['username'],
        'expiration': str(datetime.utcnow() + timedelta(minutes=10))
    },app.config['SECRET_KEY'])
    session["token"] = token
    return make_response({
        "message": "registration success",
        "error": "",
        "code": "1"
    }, 200)


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
        username, account_number, balance = str(data[0]), str(data[2]), str(data[3])
        return make_response({
            "message": "success",
            "error": "",
            "username": username,
            "balance": balance,
            "account_number": account_number,
            "code": "1"
        }, 200)
    except Exception as e:
        # return str(e)
        return make_response({
            "message": "failed",
            "error": "not authenticated",
            "more info": str(e),
            "code": "0"
        }, 401)


@app.route("/view_transactions", methods=["GET"])
def view_transactions():
    try:
        token = session["token"]
        username, jwt_exp = str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["username"]), str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["expiration"])
        # if expiration<datetime.now():
        #     return redirect("/logout")
        cursor.execute("select account_number from users where username=\""+username+"\"")
        account_number = cursor.fetchone()[0]
        cursor.execute("select * from transactions where _from=\""+account_number+"\""+" or _to=\""+account_number+"\" ORDER BY date DESC")
        transactions = cursor.fetchall()
        return make_response({
            "message": "success",
            "error": "",
            "transactions": transactions,
            "code": "1"
        }, 200)
    except Exception as e:
        return make_response({
            "message": "failed",
            "error": "not authenticated",
            "code": "0"
        }, 401)


@app.route("/transfer", methods=["POST"])
def transfer():
    try:
        token = session["token"]
        username, jwt_exp = str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["username"]), str(dict(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))["expiration"])
        # if expiration<datetime.now():
        #     return redirect("/logout")
        try:
            req_body = request.json
            post_data = {
                "receiver": req_body["receiver"],
                "amount": int(req_body["amount"])
            }
            if post_data["amount"]<=0:
                return make_response({
                    "message": "transaction failed",
                    "error": "amount needs to be > 0",
                    "code": "0"
                }, 400)
            cursor.execute("select account_number from users")
            all_account_numbers = [item for sublist in cursor.fetchall() for item in sublist]
            if post_data["receiver"] not in all_account_numbers:
                return make_response({
                    "message": "transaction failed",
                    "error": "Receiver account not found",
                    "code": "0"
                }, 400)
            cursor.execute("select username from users where account_number=\""+post_data["receiver"]+"\"")
            receiver_name = cursor.fetchone()[0]
            cursor.execute("select account_number from users where username=\""+username+"\"")
            user_account_number = cursor.fetchone()[0]
            if post_data["receiver"] == user_account_number:
                return make_response({
                    "message": "transaction failed",
                    "error": "you cannot send money to yourself",
                    "code": "0"
                }, 400)
            cursor.execute("select balance from users where username=\""+username+"\"")
            current_balance = cursor.fetchone()[0]
            if post_data["amount"]<=current_balance:
                # cursor.execute("SET AUTOCOMMIT=0")
                connection.autocommit=False
                try:
                    # connection.start_transaction()
                    # actual transaction
                    cursor.execute("select balance from users where account_number=\""+post_data["receiver"]+"\"")
                    current_balance2 = cursor.fetchone()[0]
                    cursor.execute("update users set balance={} where account_number=\"{}\"".format(current_balance2+post_data["amount"], post_data["receiver"]))
                    cursor.execute("update users set balance={} where username=\"{}\"".format(current_balance-post_data["amount"], username))
                    cursor.execute("select count(*) from transactions")
                    transaction_number = 1+int(cursor.fetchone()[0])
                    cursor.execute("select account_number from users where username=\""+username+"\"")
                    sender_account = cursor.fetchone()[0]
                    cursor.execute("insert into transactions values({}, \"{}\", \"{}\", \"{}\", {})".format(transaction_number, str(datetime.now()), sender_account, post_data["receiver"], post_data["amount"]))
                    connection.commit()
                    return make_response({
                        "message": "transaction success: ${} sent to {}".format(post_data["amount"], receiver_name),
                        "error": "",
                        "code": "1"
                    }, 200)
                except Exception as e:
                    connection.rollback()
                    return make_response({
                        "message": "transaction failed",
                        "error": str(e),
                        "code": "0"
                    }, 400)
                cursor.execute("SET AUTOCOMMIT=1")
            else:
                return make_response({
                    "message": "transaction failed",
                    "error": "insufficied balance",
                    "code": "0"
                }, 400)
        except Exception as e:
            return make_response({
                "message": "transaction failed",
                "error": str(e),
                "code": "0"
            }, 400)
    except:
        return make_response({
            "message": "transaction failed",
            "error": "not authenticated",
            "code": "0"
        }, 401)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)