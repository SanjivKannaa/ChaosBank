from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from extensions import db
from models import User
from argon2 import PasswordHasher

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["username", "profileName", "password", "email", "phoneNumber", "securityQuestion1", "securityQuestion2", "securityQuestion3"]
    if any(field not in data or not data[field] for field in required_fields):
        return jsonify({"error": "Not all fields available"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already used"}), 400

    hashed_password = ph.hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password, profileName=data["profileName"],
                    email=data["email"], phoneNumber=data["phoneNumber"],
                    securityQuestion1=data["securityQuestion1"], securityQuestion2=data["securityQuestion2"],
                    securityQuestion3=data["securityQuestion3"])
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=data["username"])
    return make_response(jsonify({"message": "User registered successfully", "jwt": access_token}), 201)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Not all fields available"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 401

    try:
        ph.verify(user.password, data["password"])
    except:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=data["username"])
    return make_response(jsonify({"message": "Login successful", "jwt": access_token}))
