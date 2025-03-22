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


    # Return the user details along with transaction information
    return make_response(jsonify({
        "username": username,
        "profileName": profileName,
        "email": email,
        "phoneNumber": phoneNumber,
        "balance": balance,
        "accountNumber": accountNumber,
    }))