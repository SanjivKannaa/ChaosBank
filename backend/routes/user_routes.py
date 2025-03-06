from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transaction
from extensions import db
from datetime import datetime, timedelta

user_bp = Blueprint('user', __name__)

@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    email = user.email
    phoneNumber = user.phoneNumber
    profileName = user.profileName
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
        "profileName": profileName,
        "email": email,
        "phoneNumber": phoneNumber,
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