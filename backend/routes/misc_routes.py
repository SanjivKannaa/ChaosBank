from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from extensions import db

misc_bp = Blueprint('misc', __name__)

@misc_bp.route("/isUsernameAvailable", methods=["GET"])
def isUsernameAvailable():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already used"}), 400
    return jsonify({"message": "Username is available"}), 200

@misc_bp.route("/getProfileNameFromUsername", methods=["GET"])
@jwt_required()
def getProfileNameFromUsername():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"profileName": user.profileName}), 200
    else:
        return jsonify({"error": "User not found"}), 400

@misc_bp.get("/getProfileNameFromUserId")
def getProfileNameFromUserId():
    user_id = request.args.get("userId")  # Get userId from query parameters
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    user = User.query.filter_by(userId=user_id).first()
    if user:
        return jsonify({"profileName": user.profileName}), 200
    return jsonify({"error": "User not found"}), 404

@misc_bp.route("/getUserIdFromUsername", methods=["GET"])
@jwt_required()
def getUserIdFromUsername():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return jsonify({"userId": user.userId}) if user else jsonify({"error": "User not found"}), 404