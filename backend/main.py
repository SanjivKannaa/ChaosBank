from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, JWTManager
)
from flask_cors import CORS
from argon2 import PasswordHasher
from datetime import *
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{getenv('MYSQL_USER')}:{getenv('MYSQL_PASSWORD')}@mysql/{getenv('MYSQL_DATABASE')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

# Initialize Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

# Argon2 Hasher
ph = PasswordHasher()

# User Model
class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)

class Transaction(db.Model):
    transId = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    def __init__(self, sender, receiver, amount, timeStamp):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timeStamp = timeStamp

# Create tables (if running for the first time)
with app.app_context():
    db.create_all()

# Register Route
@app.post("/register")
def register():
    data = request.json
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Not all fields available"}), 400
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = ph.hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    response = make_response(jsonify({
            "message": "User registered successfully",
            "jwt": access_token
        }), 201)
    # response.set_cookie("jwt", access_token, httponly=True, secure=False, samesite="None", max_age=1800)
    # response.set_cookie("refresh", refresh_token, httponly=True, secure=False, samesite="None", max_age=86400)
    return response

# Login Route
@app.post("/login")
def login():
    data = request.json
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Not all fields available"}), 400
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 401

    try:
        ph.verify(user.password, password)
    except:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    response = make_response(jsonify({
            "message": "Login successful",
            "jwt": access_token
        }))
    # response.set_cookie("jwt", access_token, httponly=True, secure=False, samesite="None", max_age=1800)
    # response.set_cookie("refresh", refresh_token, httponly=True, secure=False, samesite="None", max_age=86400)
    return response

@app.get("/dashboard")
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    balance = user.balance
    accountNumber = user.userId

    today = datetime.today()

    # **This Month**: From the start of the current month to now
    start_of_month = today.replace(day=1)
    transactions_this_month = Transaction.query.filter(
        (Transaction.sender == user.userId) | (Transaction.receiver == user.userId),
        Transaction.timeStamp >= start_of_month
    ).all()

    # Calculate total credit and total debit for this month
    total_credit_this_month = sum(t.amount for t in transactions_this_month if t.receiver == user.userId)
    total_debit_this_month = sum(t.amount for t in transactions_this_month if t.sender == user.userId)

    # **Last Month**: From the start of the previous month to the end of the previous month
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    transactions_last_month = Transaction.query.filter(
        (Transaction.sender == user.userId) | (Transaction.receiver == user.userId),
        Transaction.timeStamp >= first_day_last_month,
        Transaction.timeStamp <= last_day_last_month
    ).all()

    # Calculate total credit and total debit for last month
    total_credit_last_month = sum(t.amount for t in transactions_last_month if t.receiver == user.userId)
    total_debit_last_month = sum(t.amount for t in transactions_last_month if t.sender == user.userId)

    # **Last 6 Months**: From 6 months ago to now
    start_of_last_6_months = today - timedelta(days=6*30)  # Roughly 6 months ago
    transactions_last_6_months = Transaction.query.filter(
        (Transaction.sender == user.userId) | (Transaction.receiver == user.userId),
        Transaction.timeStamp >= start_of_last_6_months
    ).all()

    # Calculate total credit and total debit for last 6 months
    total_credit_last_6_months = sum(t.amount for t in transactions_last_6_months if t.receiver == user.userId)
    total_debit_last_6_months = sum(t.amount for t in transactions_last_6_months if t.sender == user.userId)

    # **This Year**: From the start of the current year to now
    start_of_year = today.replace(month=1, day=1)
    transactions_this_year = Transaction.query.filter(
        (Transaction.sender == user.userId) | (Transaction.receiver == user.userId),
        Transaction.timeStamp >= start_of_year
    ).all()

    # Calculate total credit and total debit for this year
    total_credit_this_year = sum(t.amount for t in transactions_this_year if t.receiver == user.userId)
    total_debit_this_year = sum(t.amount for t in transactions_this_year if t.sender == user.userId)

    # Query the most recent transaction timestamp
    last_transaction = Transaction.query.filter(
        (Transaction.sender == user.userId) | (Transaction.receiver == user.userId)
    ).order_by(Transaction.timeStamp.desc()).first()

    last_transaction_timestamp = last_transaction.timeStamp if last_transaction else None

    # Return the user details along with transaction information
    return make_response(jsonify({
        "username": username,
        "balance": balance,
        "accountNumber": accountNumber,
        "totalCreditThisMonth": total_credit_this_month,
        "totalDebitThisMonth": total_debit_this_month,
        "totalCreditLastMonth": total_credit_last_month,
        "totalDebitLastMonth": total_debit_last_month,
        "totalCreditLast6Months": total_credit_last_6_months,
        "totalDebitLast6Months": total_debit_last_6_months,
        "totalCreditThisYear": total_credit_this_year,
        "totalDebitThisYear": total_debit_this_year,
        "lastTransactionTimestamp": last_transaction_timestamp
    }))

@app.post("/transaction")
@jwt_required()
def create_transaction():
    try:
        sender_username = get_jwt_identity()

        data = request.get_json()
        receiverId = data.get('receiverId')
        amount = data.get('amount')

        if not receiverId or not amount:
            return jsonify({"error": "Receiver user ID and amount are required"}), 400

        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400

        sender = User.query.filter_by(username=sender_username).first()
        receiver = User.query.filter_by(userId=receiverId).first()

        if not sender or not receiver:
            return jsonify({"error": "Sender or receiver not found"}), 404

        if sender.balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        transaction = Transaction(

            sender=sender.userId,
            receiver=receiver.userId,
            amount=amount,
            timeStamp=datetime.utcnow()
        )

        sender.balance -= amount
        receiver.balance += amount

        db.session.add(transaction)
        db.session.commit()

        return make_response(jsonify({
            "transactionId": transaction.transId,
            "message": "Transaction successful",
            "amount": amount,
            "sender_balance": sender.balance,
        }))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import request, jsonify, make_response
from datetime import datetime

@app.get("/transactionHistory")
@jwt_required()
def transaction_history():
    try:
        # Get the current user based on the JWT identity
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get the JSON data from the request, or use an empty dictionary if no JSON is provided
        data = request.get_json() or {}

        # Get the 'fromDate' and 'toDate' filters from the request body, if available
        fromDate = data.get('fromDate')  # Optional filter for start date (YYYY-MM-DD)
        toDate = data.get('toDate')  # Optional filter for end date (YYYY-MM-DD)

        # Start building the query filter
        query = Transaction.query.filter(
            (Transaction.sender == user.userId) | (Transaction.receiver == user.userId)
        )

        # Apply filters if present
        if fromDate:
            fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
            query = query.filter(Transaction.timeStamp >= fromDate)
        
        if toDate:
            toDate = datetime.strptime(toDate, "%Y-%m-%d")
            query = query.filter(Transaction.timeStamp <= toDate)

        # Fetch the transactions
        transactions = query.all()

        # If no transactions, return an appropriate message
        if not transactions:
            return jsonify({"message": "No transactions found for the specified date range"}), 404

        # Serialize the transaction data to send back in the response
        transaction_history = [{
            "transaction_id": t.transId,
            "sender": t.sender,
            "receiver": t.receiver,
            "amount": t.amount,
            "timestamp": t.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
        } for t in transactions]

        return make_response(jsonify(transaction_history))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)