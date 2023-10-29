#!/usr/bin/python3
"""
Flask route is returns json stat response
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
from api.v1.views.base_actions import REST_actions


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_der_pla(place_id=None):
    """
        reviews route to handle http method for requ rev by place
    """
    placed_obdj = storage.get('Place', place_id)

    if request.method == 'GET':
        if placed_obdj is None:
            abort(404, 'Not found')
        all_amenities = storage.all('Amenity')
        if STORAGE_T == 'db':
            place_amenities = placed_obdj.amenities
        else:
            place_amen_ids = placed_obdj.amenities
            place_amenities = []
            for amen in place_amen_ids:
                response.append(storage.get('Amenity', amen))
        place_amenities = [
            obdj.to_json() for obdj in place_amenities
            ]
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_todo_plac(place_id=None, amenity_id=None):
    """
        reviews route to handle http meth for giv revi ID
    """
    placed_obdj = storage.get('Place', place_id)
    amenity_obdj = storage.get('Amenity', amenity_id)
    if placed_obdj is None:
        abort(404, 'Not found')
    if amenity_obdj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (amenity_obdj not in placed_obdj.amenities and
                amenity_obdj.id not in placed_obdj.amenities):
            abort(404, 'Not found')
        if STORAGE_T == 'db':
            placed_obdj.amenities.remove(amenity_obdj)
        else:
            placed_obdj.amenity_ids.pop(amenity_obdj.id, None)
        placed_obdj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity_obdj in placed_obdj.amenities or
                amenity_obdj.id in placed_obdj.amenities):
            return jsonify(amenity_obdj.to_json()), 200
        if STORAGE_T == 'db':
            placed_obdj.amenities.append(amenity_obdj)
        else:
            placed_obdj.amenities = amenity_obdj
        return jsonify(amenity_obdj.to_json()), 201
