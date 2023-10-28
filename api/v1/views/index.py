#!/usr/bin/python3
"""this module handles status and stats routs"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns a JSON says the status of the API is OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each object"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage

    classes = [('amenities', Amenity), ('cities', City),
               ('places', Place,), ('reviews', Review,),
               ('states', State), ('users', User)]
    stats_dict = {}
    for key, cls_object in classes:
        stats_dict[key] = storage.count(cls_object)
    return jsonify(stats_dict)
