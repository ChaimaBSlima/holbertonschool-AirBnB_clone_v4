#!/usr/bin/python3
""" New view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import Flask, jsonify, abort, request


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def retrieve_cities(state_id):
    """Retrieve all City objects"""
    statesdict = storage.get(State, state_id)
    if statesdict is None:
        abort(404)
    city_list = []
    all_cities = storage.all(City)
    for city in all_cities.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def retrieve_city_object(city_id):
    """Retrieve a City object based on id"""
    citiesdict = storage.get(City, city_id)
    if citiesdict is None:
        abort(404)
    else:
        citiesdictjs = citiesdict.to_dict()
        return jsonify(citiesdictjs)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city_object(city_id):
    """deletes a City object based on id"""
    citiesdict = storage.get(City, city_id)
    if not citiesdict:
        abort(404)
    else:
        storage.delete(citiesdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_a_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    data.update({"state_id": state_id})
    newcity = City(**data)
    storage.save()
    return jsonify(newcity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    ignored = ["id", "updated_at", "created_at"]
    citiesdict = storage.get(City, city_id)
    if not citiesdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(citiesdict, key, value)
                storage.save()
        return jsonify(citiesdict.to_dict()), 200
