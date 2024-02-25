#!/usr/bin/python3
""" stts """

from api.v1.views import app_views
from flask import jsonify, request, abort
import models

@app_views.route("/states/<state_id>/cities", methods=["GET","POST"], strict_slashes=False)
def state_cities_route(state_id=None):
    state_id = f'State.{state_id}'
    state = models.storage.all(models.state.State).get(state_id)
    
    if state is None:
        abort(404)
    
    if request.method == "GET":
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    elif request.method == "POST":
        try:
            req = request.get_json()  
        except Exception as e :
            abort(400,{"error":"Not a JSON"})
        
        if "name" not in req.keys():
            abort(400,{"error":"Missing name"})
        
        city = models.city.City(req)
        models.storage.new(city)
        models.storage.save()
        
        return jsonify(city.to_dict()), 201
            
    return jsonify({}), 200

@app_views.route("/cities/<city_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
def cities_route(city_id):
    city_id = f'State.{city_id}'
    city = models.storage.all(models.city.City).get(city_id)
    
    if state is None:
        abort(404)
    
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "PUT":
        try:
            req = request.get_json()  
        except Exception as e :
            abort(400,{"error":"Not a JSON"})
        
        if "name" not in req.keys():
            abort(400,{"error":"Missing name"})
        
        for k,v in req.items():
            city.__setattr__(k,v)
        city.save()
        
        return jsonify(city.to_dict()), 200
    else:
        models.storage.delete(city)
        models.storage.save()
        
    return jsonify({}), 200
"""
Retrieves a City object. : GET /api/v1/cities/<city_id>

    If the city_id is not linked to any City object, raise a 404 error

Deletes a City object: DELETE /api/v1/cities/<city_id>

    If the city_id is not linked to any City object, raise a 404 error
    Returns an empty dictionary with the status code 200

Updates a City object: PUT /api/v1/cities/<city_id>

    If the city_id is not linked to any City object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP body request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the City object with all key-value pairs of the dictionary
    Ignore keys: id, state_id, created_at and updated_at
    Returns the City object with the status code 200

 """