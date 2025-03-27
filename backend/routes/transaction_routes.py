from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transaction
from extensions import db
from datetime import datetime, timedelta

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/transfer", methods=["POST"])
@jwt_required()
def create_transaction():
    sender_username = get_jwt_identity()
    data = request.get_json()

    sender = User.query.filter_by(username=sender_username).first()
    receiver = User.query.filter_by(userId=data.get('receiverId')).first()

    if not sender or not receiver or sender.userId == receiver.userId or sender.balance < int(data.get('amount')):
        return jsonify({"error": "Invalid transaction"}), 400

    transaction = Transaction(sender=sender.userId, receiver=receiver.userId, amount=int(data.get('amount')))
    sender.balance -= transaction.amount
    receiver.balance += transaction.amount

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction successful", "transactionId": transaction.transId})

@transaction_bp.route("/transactionHistory", methods=["POST"])
@jwt_required()
def transaction_history():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    data = request.get_json() or {}
    fromDate = datetime.strptime(data.get('fromDate'), "%Y-%m-%d") if data.get('fromDate') else None
    toDate = datetime.strptime(data.get('toDate'), "%Y-%m-%d") if data.get('toDate') else None

    query = Transaction.query.filter((Transaction.sender == user.userId) | (Transaction.receiver == user.userId))
    if fromDate:
        query = query.filter(Transaction.timeStamp >= fromDate)
    if toDate:
        query = query.filter(Transaction.timeStamp <= toDate)

    transactions = query.all()
    return jsonify([{
        "transaction_id": t.transId,
        "sender": User.query.get(t.sender).username+"["+str(User.query.get(t.sender).userId)+"]",
        "receiver": User.query.get(t.receiver).username+"["+str(User.query.get(t.receiver).userId)+"]",
        "amount": t.amount,
        "timestamp": t.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
    } for t in transactions[::-1]])

@transaction_bp.route("/lastTenTransactions", methods=["GET"])
@jwt_required()
def lastTenTransactions():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    query = Transaction.query.filter((Transaction.sender == user.userId) | (Transaction.receiver == user.userId))

    transactions = query.order_by(Transaction.timeStamp.desc()).limit(10).all()
    return jsonify([{
        "transaction_id": t.transId,
        "sender": User.query.get(t.sender).username,
        "receiver": User.query.get(t.receiver).username,
        "amount": t.amount,
        "timestamp": t.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
    } for t in transactions])

@transaction_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

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

@transaction_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit():
    sender_username = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    user = User.query.filter_by(username=sender_username).first()

    if not user:
        return jsonify({"error": "Account not found!"}), 400

    user.balance += amount

    db.session.commit()

    return jsonify({"message": "Deposit successful"})

@transaction_bp.route("/withdraw", methods=["POST"])
@jwt_required()
def credit():
    sender_username = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    user = User.query.filter_by(username=sender_username).first()

    if not user:
        return jsonify({"error": "Account not found!"}), 400

    user.balance -= amount

    db.session.commit()

    return jsonify({"message": "withdrawal successful"})
