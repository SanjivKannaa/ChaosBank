from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Transaction
from extensions import db
from datetime import datetime

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
        "sender": User.query.get(t.sender).profileName+"["+User.query.get(t.sender).username+"]",
        "receiver": User.query.get(t.receiver).profileName+"["+User.query.get(t.receiver).username+"]",
        "amount": t.amount,
        "timestamp": t.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
    } for t in transactions])
