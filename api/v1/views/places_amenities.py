#!/usr/bin/python3
"""
Flask route that returns JSON status response
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_perds_place(place_id=None):
    """
    Route to handle HTTP method for retrieving amenities by place
    """
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404, 'Not found')

    place_amenities = place_obj.amenities
    amenities_json = [amenity.to_dict() for amenity in place_amenities]
    return jsonify(amenities_json)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_tis_place(place_id=None,
                      amenity_id=None):

    """
    Route to handle HTTP methods for a given amenity by ID
    """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if place_obj is None or amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404, 'Not found')

        place_obj.amenities.remove(amenity_obj)
        place_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200

        place_obj.amenities.append(amenity_obj)
        place_obj.save()
        return jsonify(amenity_obj.to_dict()), 201
