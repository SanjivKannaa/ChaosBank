import os
os.system("pip3 install flask")
from flask import Flask, render_template, jsonify


app = Flask(__name__)

@app.get("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)