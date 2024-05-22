import os
os.system("pip3 install flask")
os.system("pip3 install pyjwt")
from flask import Flask, request, jsonify, make_response, request, render_template, session, flash, redirect
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'u39u5gh3#RF#*35f#F*#%n3u3f3n59u35f#F#G3'

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