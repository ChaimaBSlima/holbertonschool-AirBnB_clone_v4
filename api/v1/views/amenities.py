#!/usr/bin/python3
""" New view for Amenity objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import Flask, jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_amenities():
    """Retrieve all Amenity objects"""
    amenitiesdict = storage.all(Amenity)
    amenitieslist = []
    for key, value in amenitiesdict.items():
        amenitieslist.append(value.to_dict())
    return jsonify(amenitieslist)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def retrieve_amenity_object(amenity_id):
    """Retrieve an Amenity object based on id"""
    amenitiesdict = storage.get(Amenity, amenity_id)
    if amenitiesdict is None:
        abort(404)
    else:
        amenitiesdictjs = amenitiesdict.to_dict()
        return jsonify(amenitiesdictjs)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_obj(amenity_id):
    """deletes an Amenity object based on id"""
    amenitiesdict = storage.get(Amenity, amenity_id)
    if not amenitiesdict:
        abort(404)
    else:
        storage.delete(amenitiesdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    newamenity = Amenity(**data)
    storage.save()
    return jsonify(newamenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    ignored = ["id", "updated_at", "created_at"]
    amenitiesdict = storage.get(Amenity, amenity_id)
    if not amenitiesdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(amenitiesdict, key, value)
                storage.save()
        return jsonify(amenitiesdict.to_dict()), 200
