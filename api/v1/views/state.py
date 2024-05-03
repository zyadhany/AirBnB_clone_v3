#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/')
def list_states():
    '''get all states'''
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''get id'''
    state = storage.get(State, state_id).values()
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a State object'''
    state = storage.get(State, state_id).values()
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200
