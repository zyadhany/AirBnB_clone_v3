#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from datetime import datetime
import uuid


@app_views.route('/cities/', methods=['GET'])
def list_states():
    '''get all cities'''
    cities = [obj.to_dict() for obj in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/cities/<state_id>', methods=['GET'])
def get_state(state_id):
    '''get id'''
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a City object'''
    city = storage.get(City, state_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_state():
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = City(name=request.json['name'])
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Updates a City object'''
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city.name = request.json['name']
    city.save()
    return jsonify(city.to_dict()), 200
