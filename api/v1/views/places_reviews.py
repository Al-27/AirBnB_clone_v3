#!/usr/bin/python3
"""
Create a new view for Review object that handles all default RESTFul API actions:

    In the file api/v1/views/places_reviews.py
    You must use to_dict() to retrieve an object into valid JSON
    Update api/v1/views/__init__.py to import this new file

Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews

    If the place_id is not linked to any Place object, raise a 404 error

Creates a Review: POST /api/v1/places/<place_id>/reviews

    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the place_id is not linked to any Place object, raise a 404 error
    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object, raise a 404 error
    If the dictionary doesn’t contain the key text, raise a 400 error with the message Missing text
    Returns the new Review with the status code 201

"""
from flask import Flask, request, abort, jsonify
from . import app_views
import models

@app_views.route("/places/<place_id>/reviews",methods=["GET","POST"], strict_slashes=False)
def place_reviews_route(place_id):
    place = models.storage.get("Place", f"Place.{place_id}")
    if place is None:
        abort(404)
    
    if request.method == "GET":
        reviews = []
        for rev in place.reviews:
            reviews.append(rev.to_dict())
        return jsonify(reviews)
    else:
        try:
            req = request.get_json()
        except Exception:
            abort(400, {"error": "Not a JSON"})
            
        for k in ["user_id", "text"]:
            if k not in req.keys():
                abort(400, {"error": f"Missing {k}"})
        user = models.storage.get("User",f'User.{req["user_id"]}')
        if user is None:
            abort(404)

        review = models.review.Review(**req)
        review.save()
        
        return jsonify(review.to_dict()), 201
        
    return jsonify({})
        
    
"""
Retrieves a Review object. : GET /api/v1/reviews/<review_id>

    If the review_id is not linked to any Review object, raise a 404 error

Deletes a Review object: DELETE /api/v1/reviews/<review_id>

    If the review_id is not linked to any Review object, raise a 404 error
    Returns an empty dictionary with the status code 200

Updates a Review object: PUT /api/v1/reviews/<review_id>

    If the review_id is not linked to any Review object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the Review object with all key-value pairs of the dictionary
    Ignore keys: id, user_id, place_id, created_at and updated_at
    Returns the Review object with the status code 200
"""