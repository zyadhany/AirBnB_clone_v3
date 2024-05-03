#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def list_reviews_of_place(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Retrieves a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''Creates a Review'''
    if not request.get_json():
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, 'Missing text')

    review = Review(user_id=user.id,
                    place_id=place.id, text=request.get_json()['text'])
    storage.save(review)
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    '''Updates a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    update_dict = request.get_json()
    # Ignore update for id, user_id, place_id, created_at and updated_at
    for key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
        update_dict.pop(key, None)

    for key, value in update_dict.items():
        setattr(review, key, value)

    storage.save(review)
    return jsonify(review.to_dict()), 200
