#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users', methods=['GET'])
def list_users():
    '''Retrieves the list of all User objects'''
    users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Retrieves a User object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a User object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    '''Creates a User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')

    user = User(email=request.json['email'], password=request.json['password'])
    storage.save(user)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates a User object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    # Ignore update for id, email, created_at and updated_at
    update_dict = request.get_json()
    for key in ['id', 'email', 'created_at', 'updated_at']:
        update_dict.pop(key, None)

    for key, value in update_dict.items():
        setattr(user, key, value)

    storage.save(user)
    return jsonify(user.to_dict()), 200
