#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid



@app_views.route('/states/', methods=['GET'])
def list_states():
    '''Retrieves the list of all State objects'''
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''Retrieves a specific State object by its ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "State not found")  # More descriptive error message
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a specific State object by its ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "State not found")
    storage.delete(state)
    storage.save()
    return jsonify({}), 200  # Empty response with success code


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates a new State object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    new_state = State(name=request.json['name'])
    storage.save(new_state)
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''Updates an existing State object by its ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "State not found")
    if not request.get_json():
        abort(400, 'Not a JSON')

    # Update only allowed fields (avoid unintended modifications)
    update_dict = request.get_json()
    allowed_fields = ['name']
    for key in update_dict.keys():
        if key not in allowed_fields:
            return abort(400, f"Update for '{key}' not allowed")

    for key, value in update_dict.items():
        setattr(state, key, value)

    storage.save(state)
    return jsonify(state.to_dict()), 200
