from flask import Blueprint, request, jsonify
from extensions import db
from models import Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['POST'])
def create_notification():
    data = request.json
    new_notification = Notification(user_id=data['user_id'], message=data['message'])
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({"message": "Notification created"}), 201

@notification_bp.route('/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": notif.id, "message": notif.message, "is_read": notif.is_read} for notif in notifications]), 200
