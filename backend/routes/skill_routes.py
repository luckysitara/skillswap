from flask import Blueprint, request, jsonify
from extensions import db
from models import Skill

skill_bp = Blueprint('skill', __name__)

@skill_bp.route('/', methods=['POST'])
def create_skill():
    data = request.json
    new_skill = Skill(name=data['name'], user_id=data['user_id'])
    db.session.add(new_skill)
    db.session.commit()
    return jsonify({"message": "Skill created"}), 201

@skill_bp.route('/<int:user_id>', methods=['GET'])
def get_skills(user_id):
    skills = Skill.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": skill.id, "name": skill.name} for skill in skills]), 200
