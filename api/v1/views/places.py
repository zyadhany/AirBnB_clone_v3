#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    place = Place(user_id=user.id, city_id=city.id,
                  name=request.get_json()['name'])
    storage.save(place)
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Updates a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    update_dict = request.get_json()
    # Ignore update for id, user_id, city_id, created_at and updated_at
    for key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
        update_dict.pop(key, None)

    for key, value in update_dict.items():
        setattr(place, key, value)

    storage.save(place)
    return jsonify(place.to_dict()), 200
