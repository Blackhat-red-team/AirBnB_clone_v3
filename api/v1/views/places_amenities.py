#!/usr/bin/python3
"""handles all default RESTFul API actions for Place objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views.base_actions import REST_actions
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def get_place_amenities(place_id):
    """get place amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities_dict = list(map(lambda a: a.to_dict(), place.amenities))

    return jsonify(amenities_dict)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """delete place amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        place_amenity = None
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                place_amenity = amenity
                break
        if place_amenity is None:
            abort(404)
        storage.delete(place_amenity)
    else:
        try:
            place.amenity_ids.remove(amenity_id)
        except Exception as e:
            abort(404)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """post place amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage_t = getenv("HBNB_TYPE_STORAGE")
    status_code = 200
    if storage_t == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            status_code = 201
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            storage.save()
            status_code = 201

    return jsonify(amenity.to_dict()), status_code
