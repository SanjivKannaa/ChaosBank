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
    date_of_birth = db.Column(db.Date, nullable=True)
    door_plot_no = db.Column(db.String(20), nullable=True)
    street_name_1 = db.Column(db.String(100), nullable=True)
    street_name_2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    pin = db.Column(db.String(10), nullable=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    aadhar_number = db.Column(db.String(12), unique=True, nullable=True)
    pan_number = db.Column(db.String(10), unique=True, nullable=True)


class Transaction(db.Model):
    transId = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
