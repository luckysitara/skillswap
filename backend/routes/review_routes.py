from flask import Blueprint, request, jsonify
from extensions import db
from models import Review

review_bp = Blueprint('review', __name__)

@review_bp.route('/', methods=['POST'])
def leave_review():
    data = request.json
    new_review = Review(reviewer_id=data['reviewer_id'], reviewee_id=data['reviewee_id'], content=data['content'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review submitted"}), 201

@review_bp.route('/<int:reviewee_id>', methods=['GET'])
def get_reviews(reviewee_id):
    reviews = Review.query.filter_by(reviewee_id=reviewee_id).all()
    return jsonify([{"id": review.id, "content": review.content} for review in reviews]), 200
