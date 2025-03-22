from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from extensions import db
from models import User
from argon2 import PasswordHasher
import re

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["username", "profileName", "password", "email", "phoneNumber"]
    if any(field not in data or not data[field] for field in required_fields):
        return jsonify({"error": "Not all fields available"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already used"}), 400
    
    def is_strong_password(password):
        # Password strength criteria
        min_length = 8
        has_upper = re.search(r"[A-Z]", password)
        has_lower = re.search(r"[a-z]", password)
        has_digit = re.search(r"\d", password)
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        # Collect errors for better debugging
        errors = []
        if len(password) < min_length:
            errors.append("Password must be at least 8 characters long.")
        if not has_upper:
            errors.append("Password must contain at least one uppercase letter.")
        if not has_lower:
            errors.append("Password must contain at least one lowercase letter.")
        if not has_digit:
            errors.append("Password must contain at least one digit.")
        if not has_special:
            errors.append("Password must contain at least one special character.")

        return errors

    # Validate password strength
    password_errors = is_strong_password(data["password"])
    if password_errors:
        return make_response(jsonify({"error": " ".join(password_errors)}), 400)

    hashed_password = ph.hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password, profileName=data["profileName"], email=data["email"], phoneNumber=data["phoneNumber"])
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
