from extensions import db
from datetime import datetime

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    profileName = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phoneNumber = db.Column(db.String(10), unique=True, nullable=True)
    balance = db.Column(db.Integer, nullable=False, default=1000)

class Transaction(db.Model):
    transId = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
