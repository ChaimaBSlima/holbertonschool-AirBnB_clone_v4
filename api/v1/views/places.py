#!/usr/bin/python3
""" New view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import Flask, jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def retrieve_places(city_id):
    """Retrieve all Place objects"""
    citiesdict = storage.get(City, city_id)
    if citiesdict is None:
        abort(404)
    place_list = []
    all_places = storage.all(Place)
    for place in all_places.values():
        if place.city_id == city_id:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def retrieve_place_object(place_id):
    """Retrieve a Place object based on id"""
    placesdict = storage.get(Place, place_id)
    if placesdict is None:
        abort(404)
    else:
        placesdictjs = placesdict.to_dict()
        return jsonify(placesdictjs)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_object(place_id):
    """deletes a Place object based on id"""
    placesdict = storage.get(Place, place_id)
    if not placesdict:
        abort(404)
    else:
        storage.delete(placesdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_a_place(city_id):
    """Creates a new Place object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if "user_id" not in data:
        abort(400, "Missing name")
    if "name" not in data:
        abort(400, "Missing name")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    data["city_id"] = city_id
    new_place = Place(**data)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    ignored = ["id", "updated_at", "created_at", "user_id", "city_id"]
    placesdict = storage.get(Place, place_id)
    if not placesdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(placesdict, key, value)
                storage.save()
        return jsonify(placesdict.to_dict()), 200
