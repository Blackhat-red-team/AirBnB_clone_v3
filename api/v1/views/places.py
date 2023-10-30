#!/usr/bin/python3
"""handles all default RESTFul API actions for Place objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from api.v1.views.base_actions import REST_actions
from os import getenv


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """gets a Place object by its id"""
    place = REST_actions.get_by_id(Place, place_id)
    if place.get('status code') == 404:
        abort(404)
    return jsonify(place.get('object dict'))


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """gets all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # craete a list of dictionaries
    places = list(map(lambda place: place.to_dict(), city.places))
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a Place object by its id"""
    delete_response = REST_actions.delete(Place, place_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_body = request.get_json()
    if request_body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    if not request_body.get('name'):
        return jsonify({'error': 'Missing name'}), 400
    user = storage.get(User, request_body.get('user_id'))
    if user is None:
        abort(404)
    new_place = Place(name=request_body.get('name'), user_id=user.id,
                      city_id=city_id)
    post_response = REST_actions.post(new_place)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ updates a Place object by its id """
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    args_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        Place, place_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """creates a Place"""

    request_body = request.get_json()
    if request_body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    # body values
    body_states = request_body.get('states', [])
    body_cities = request_body.get('cities', [])
    body_amenities = request_body.get('amenities', [])

    # if there are no states, cities or amenities or empty body
    if request_body == {} or (body_states == [] and
                              body_cities == [] and body_amenities == []):
        all_places = storage.all(Place)
        all_places_list = list(map(lambda p: p.to_dict(), all_places.values()))
        return jsonify(all_places_list)

    places = []
    if body_states == [] and body_cities == []:
        places = list(map(lambda p: p, storage.all(Place).values()))
    else:
        # get all cities ids for the states
        for state_id in body_states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
        # get places from body cities
        for city_id in body_cities:
            # if city_id is not in cities_places
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)
    places = list(set(places))
    # filter by amenities
    if body_amenities:
        places_with_amenities = []
        for place in places:
            # amenities is of type Amenity
            if getenv("HBNB_TYPE_STORAGE") == "db":
                if all(list(map(lambda a: a in
                                list(map(lambda c: c.id, place.amenities)),
                                body_amenities))):
                    # delete amenities from place dict
                    del place.amenities
                    places_with_amenities.append(place.to_dict())
            else:
                if all(list(map(lambda a: a in place.amenities,
                                body_amenities))):
                    # delete amenities from place dict
                    del place.amenities
                    places_with_amenities.append(place.to_dict())
        return jsonify(places_with_amenities)
    else:
        # return all places
        places_list = list(map(lambda p: p.to_dict(), places))
        return jsonify(places_list)
