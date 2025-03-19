from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from extensions import db
from models import User
from argon2 import PasswordHasher
import re

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = [
        "username", "date_of_birth", "address", "mobile_number", "aadhar_number", "pan_number", "profileName", "password", "phoneNumber", "balance", "email"
    ]
    
    address_fields = [
        "door_plot_no", "street_name_1", "street_name_2", "city", "state", "country", "pin"
    ]
    
    if any(field not in data or not data[field] for field in required_fields):
        return jsonify({"error": "Not all fields available"}), 400
    
    if any(field not in data["address"] or not data["address"][field] for field in address_fields):
        return jsonify({"error": "Incomplete address information"}), 400
    
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
    new_user = User(
        username=data["username"],
        profileName=data["profileName"],
        password=hashed_password,
        phoneNumber=data["phoneNumber"],
        balance=data["balance"],
        email=data["email"],
        date_of_birth=data["date_of_birth"],
        door_plot_no=data["address"]["door_plot_no"],
        street_name_1=data["address"]["street_name_1"],
        street_name_2=data["address"]["street_name_2"],
        city=data["address"]["city"],
        state=data["address"]["state"],
        country=data["address"]["country"],
        pin=data["address"]["pin"],
        mobile_number=data["mobile_number"],
        aadhar_number=data["aadhar_number"],
        pan_number=data["pan_number"]
    )
    
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
