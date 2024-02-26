#!/usr/bin/python3
""" places doc """

from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
import models 

@app_views.route("/cities/<city_id>/places", methods=["GET","POST"], strict_slashes=False)
def city_places_rout(city_id):
    city = models.storage.all(models.city.City).get(f"City.{city_id}")
    
    if city is None:
        abort(404)
    
    if request.method == "GET":
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    else:
        try:
            req = request.get_json()
        except Exception:
            abort(400,{"error": "Not a JSON"})
        
        for k in ["user_id", "name"]:
            if k not in req.keys():
                abort(400, {"error": f"Missing {k}"})
        user = models.storage.all(models.user.User).get(f'User.{req["user_id"]}')
        if user is None:
            abort(404)
        
        place = models.place.Place(req)
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",methods=["GET","DELETE","PUT"],strict_slashes=False)
def places_route(place_id):
    place = models.storage.all(models.place.Place).get(f"Place.{place_id}")

"""
Retrieves a Place object. : GET /api/v1/places/<place_id>

    If the place_id is not linked to any Place object, raise a 404 error

Deletes a Place object: DELETE /api/v1/places/<place_id>

    If the place_id is not linked to any Place object, raise a 404 error
    Returns an empty dictionary with the status code 200 

Updates a Place object: PUT /api/v1/places/<place_id>

    If the place_id is not linked to any Place object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, user_id, city_id, created_at and updated_at
    Returns the Place object with the status code 200
"""