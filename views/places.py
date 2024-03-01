#!/usr/bin/python3
""" places doc """

from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
import models


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def city_places_route(city_id):
    """ str """
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
            abort(400, {"error": "Not a JSON"})

        for k in ["user_id", "name"]:
            if k not in req.keys():
                abort(400, {"error": f"Missing {k}"})
        user = models.storage.all(
            models.user.User).get(f'User.{req["user_id"]}')
        if user is None:
            abort(404)
        
        place = models.place.Place(**req)
        place.save()
        
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def places_route(place_id):
    """ str """
    place = models.storage.all(models.place.Place).get(f"Place.{place_id}")

    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        models.storage.delete(place)
        models.storage.save()
        return jsonify({}), 200
    else:
        try:
            req = request.get_json()
        except Exception:
            abort(400, {"error": "Not a JSON"})

        for k in ["id", "user_id", "city_id", "created_at ", " updated_at"]:
            if k in req.keys():
                req.pop(k)

        for k, v in req.items():
            place.__setattr__(k, v)
        place.save()

        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search_route():
    """ ................. """
    try:
        req = request.get_json()
    except Exception:
        abort(400, {'error': 'Not a JSON'})

    states = req.get('states', [])
    cities = req.get('cities', [])
    amenities = req.get('amenities', [])
    amenity_objects = []
    for amenity_id in amenities:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            amenity_objects.append(amenity)

    if states == cities == []:
        places = models.storage.all('Place').values()
    else:
        places = []
        for state_id in states:
            state = models.storage.get('State', state_id)
            state_cities = state.cities
            for city in state_cities:
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = models.storage.get('City', city_id)
            for place in city.places:
                places.append(place)

    plcs_rslt = []
    for place in places:
        place_amenities = place.amenities
        plcs_rslt.append(place.to_dict())
        for amenity in amenity_objects:
            if amenity not in place_amenities:
                plcs_rslt.pop()
                break

    return jsonify(plcs_rslt)
