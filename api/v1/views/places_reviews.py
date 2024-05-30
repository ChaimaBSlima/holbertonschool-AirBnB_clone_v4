#!/usr/bin/python3
""" New view for Reviews objects
that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from flask import Flask, jsonify, abort, request


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def retrieve_reviews(place_id):
    """Retrieve all Review objects"""
    placesdict = storage.get(Place, place_id)
    if placesdict is None:
        abort(404)
    reviewlist = []
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review.place_id == place_id:
            reviewlist.append(review.to_dict())
    return jsonify(reviewlist)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def retrieve_review_object(review_id):
    """Retrieve a Review object based on id"""
    reviewsdict = storage.get(Review, review_id)
    if reviewsdict is None:
        abort(404)
    else:
        reviewsdictjs = reviewsdict.to_dict()
        return jsonify(reviewsdictjs)


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review_object(review_id):
    """deletes a Review object based on id"""
    reviewsdict = storage.get(Review, review_id)
    if not reviewsdict:
        abort(404)
    else:
        storage.delete(reviewsdict)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_a_review(place_id):
    """Creates a new Review object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data["place_id"] = place_id
    new_review = Review(**data)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    ignored = ["id", "updated_at", "created_at", "place_id", "user_id"]
    reviewsdict = storage.get(Review, review_id)
    if not reviewsdict:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ignored:
                setattr(reviewsdict, key, value)
                storage.save()
        return jsonify(reviewsdict.to_dict()), 200
