#!/usr/bin/python3
""" New view for User objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import Flask, jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def retrieve_users():
    """Retrieve all User objects"""
    usersdict = storage.all(User)
    userslist = []
    for key, value in usersdict.items():
        userslist.append(value.to_dict())
    return jsonify(userslist)


@app_views.route("/users/<user_id>",
                 methods=["GET"], strict_slashes=False)
def retrieve_user_object(user_id):
    """Retrieve a User object based on id"""
    usersdict = storage.get(User, user_id)
    if usersdict is None:
        abort(404)
    else:
        usersdictjs = usersdict.to_dict()
        return jsonify(usersdictjs)


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user_obj(user_id):
    """deletes an Amenity object based on id"""
    usersdict = storage.get(User, user_id)
    if not usersdict:
        abort(404)
    else:
        storage.delete(usersdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, "Not a JSON")
    if "email" not in data:
        return abort(400, "Missing email")
    if "password" not in data:
        return abort(400, "Missing password")
    newuser = User(**data)
    storage.save()
    return jsonify(newuser.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    ignored = ["id", "updated_at", "created_at", "email"]
    usersdict = storage.get(User, user_id)
    if not usersdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(usersdict, key, value)
                storage.save()
        return jsonify(usersdict.to_dict()), 200
