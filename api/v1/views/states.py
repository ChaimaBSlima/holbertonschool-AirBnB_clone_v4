#!/usr/bin/python3
""" New view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import Flask, jsonify, abort, request
import json


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_states():
    """Retrieve all State objects"""
    statesdict = storage.all(State)
    stateslist = []
    for key, value in statesdict.items():
        stateslist.append(value.to_dict())
    return jsonify(stateslist)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def retrieve_state_object(state_id):
    """Retrieve a State object based on id"""
    statesdict = storage.get(State, state_id)
    if statesdict is None:
        abort(404)
    else:
        statesdictjs = statesdict.to_dict()
        return jsonify(statesdictjs)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state_object(state_id):
    """deletes a State object based on id"""
    statesdict = storage.get(State, state_id)
    if not statesdict:
        abort(404)
    else:
        storage.delete(statesdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_a_state():
    """Creates a new State object"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    newstate = State(**data)
    storage.save()
    return jsonify(newstate.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    ignored = ["id", "updated_at", "created_at"]
    statesdict = storage.get(State, state_id)
    if not statesdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(statesdict, key, value)
                storage.save()
        return jsonify(statesdict.to_dict()), 200
