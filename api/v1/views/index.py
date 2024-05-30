#!/usr/bin/python3
"""This is the main file for the application,
it sets up the API endpoints and imports necessary models and views."""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def index():
    """This endpoint returns a JSON object
    with the status of the application."""
    jsonstring = {"status": "OK"}
    return jsonify(jsonstring)


@app_views.route("/stats", strict_slashes=False)
def retrieve():
    """This endpoint returns a JSON object with the
    count of each type of object in the application."""
    dict = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(dict)
