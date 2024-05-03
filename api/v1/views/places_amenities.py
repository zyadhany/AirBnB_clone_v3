#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def list_amenities_of_place(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # Handle based on storage type (DBStorage vs. FileStorage)
    if isinstance(storage, storage.DBStorage):
        amenities = [obj.to_dict() for obj in place.amenities]
    else:
        amenity_ids = place.amenity_ids
        amenities = [storage.get
                     (Amenity, amenity_id).to_dict()
                     for amenity_id in amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_of_place(place_id, amenity_id):
    '''Deletes a Amenity object from a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # Check if Amenity is linked to the Place before deletion
    if isinstance(storage, storage.DBStorage):
        if amenity not in place.amenities:
            abort(404)
    if not isinstance(storage, storage.DBStorage):
        if amenity_id not in place.amenity_ids:
            abort(404)

    if isinstance(storage, storage.DBStorage):
        place.amenities.remove(amenity)  # DBStorage relationship deletion
    else:
        place.amenity_ids.remove(amenity_id)  # FileStorage list manipulation

    storage.save(place)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    '''Link a Amenity object to a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # Check if Amenity is already linked to the Place
    if isinstance(storage, storage.DBStorage):
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
    if not isinstance(storage, storage.DBStorage):
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

    if isinstance(storage, storage.DBStorage):
        place.amenities.append(amenity)  # DBStorage relationship linking
    else:
        place.amenity_ids.append(amenity_id)  # FileStorage list manipulation

    storage.save(place)
    return jsonify(amenity.to_dict()), 201
