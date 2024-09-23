from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@user_bp.route('/<int:user_id>', methods=['GET', 'PUT'])
def get_or_update_profile(user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        return jsonify({
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture
        })
    else:
        data = request.json
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({"message": "Profile updated"}), 200

@user_bp.route('/password/reset', methods=['POST'])
def reset_password():
    # Implement password reset logic
    return jsonify({"message": "Password reset link sent"}), 200
