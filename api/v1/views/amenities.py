#!/usr/bin/python3
""" amnts """

from api.v1.views import app_views
from flask import jsonify, request, abort
import models

@app_views.route("/amenities", methods=["GET","POST"],strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET","DELETE","PUT"],strict_slashes=False)
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
