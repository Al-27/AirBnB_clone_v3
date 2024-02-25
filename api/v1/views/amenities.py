#!/usr/bin/python3
""" amnts """

from api.v1.views import app_views
from flask import jsonify, request, abort
import models

@app_views.route("/amenities", methods=["GET","POST"])
@app_views.route("/amenities/<amenity_id>", methods=["GET","DELETE","PUT"])
def amenities_route(amenity_id=None):
    
    if amenity_id is None:
        if request.method == "GET":
            amenities = []
            for amenity in models.storage.all(models.amenity.Amenity).values():
                amenities.append(amenity.to_dict())
            return jsonify(amenities)
        else:
            try:
                req = request.get_json()  
            except Exception as e :
                abort(400,{"error":"Not a JSON"})
            
            if "name" not in req.keys():
                abort(400,{"error":"Missing name"})
            
            amenity = models.amenity.Amenity(**req)
            models.storage.new(amenity)
            models.storage.save()
            
            return jsonify(amenity.to_dict()), 201
    else:
        amenity_id = f'Amenity.{amenity_id}'
        amenity = models.storage.all(models.amenity.Amenity).get(amenity_id)
        
        if amenity is None:
            abort(404)
        
        if request.method == "GET":
            return jsonify(amenity.to_dict())
        elif request.method == "PUT":
            try:
                req = request.get_json()  
            except Exception as e :
                abort(400,{"error":"Not a JSON"})
            
            if "name" not in req.keys():
                abort(400,{"error":"Missing name"})
            
            for k,v in req.items():
                amenity.__setattr__(k,v)
            amenity.save()
            
            return jsonify(amenity.to_dict()), 200
        else:
            models.storage.delete(amenity)
            models.storage.save()
            
    return jsonify({}), 200
 

"""
Create a new view for Amenity objects that handles all default RESTFul API actions:

    In the file api/v1/views/amenities.py
    You must use to_dict() to serialize an object into valid JSON
    Update api/v1/views/__init__.py to import this new file

Retrieves the list of all Amenity objects: GET /api/v1/amenities

Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>

    If the amenity_id is not linked to any Amenity object, raise a 404 error

Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>

    If the amenity_id is not linked to any Amenity object, raise a 404 error
    Returns an empty dictionary with the status code 200

Creates a Amenity: POST /api/v1/amenities

    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
    Returns the new Amenity with the status code 201

Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>

    If the amenity_id is not linked to any Amenity object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the Amenity object with all key-value pairs of the dictionary
    Ignore keys: id, created_at and updated_at
    Returns the Amenity object with the status code 200

"""