from flask import Blueprint, request, jsonify
from extensions import db
from models import Message

message_bp = Blueprint('message', __name__)

@message_bp.route('/', methods=['POST'])
def send_message():
    data = request.json
    new_message = Message(sender_id=data['sender_id'], receiver_id=data['receiver_id'], content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent"}), 201

@message_bp.route('/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
    return jsonify([{"sender_id": msg.sender_id, "receiver_id": msg.receiver_id, "content": msg.content} for msg in messages]), 200

@message_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"}), 200
    return jsonify({"message": "Message not found"}), 404

@message_bp.route('/read/<int:message_id>', methods=['PATCH'])
def mark_as_read(message_id):
    message = Message.query.get(message_id)
    if message:
        message.is_read = True
        db.session.commit()
        return jsonify({"message": "Message marked as read"}), 200
    return jsonify({"message": "Message not found"}), 404
