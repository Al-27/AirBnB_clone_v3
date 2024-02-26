#!/usr/bin/python3
""" stts """

from api.v1.views import app_views
from flask import jsonify, request, abort
import models

@app_views.route("/states", methods=["GET","POST"],strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET","DELETE","PUT"],strict_slashes=False)
def states_route(state_id=None):
    
    if state_id is None:
        if request.method == "GET":
            states = []
            for state in models.storage.all(models.state.State).values():
                states.append(state.to_dict())
            return jsonify(states)
        else:
            try:
                req = request.get_json()  
            except Exception as e :
                abort(400,{"error":"Not a JSON"})
            
            if "name" not in req.keys():
                abort(400,{"error":"Missing name"})
            
            state = models.state.State(**req)
            models.storage.new(state)
            models.storage.save()
            
            return jsonify(state.to_dict()), 201
    else:
        state_id = f'State.{state_id}'
        state = models.storage.all(models.state.State).get(state_id)
        
        if state is None:
            abort(404)
        
        if request.method == "GET":
            return jsonify(state.to_dict())
        elif request.method == "PUT":
            try:
                req = request.get_json()  
            except Exception as e :
                abort(400,{"error":"Not a JSON"})
            
            if "name" not in req.keys():
                abort(400,{"error":"Missing name"})
            
            for k,v in req.items():
                state.__setattr__(k,v)
            state.save()
            
            return jsonify(state.to_dict()), 200
        else:
            models.storage.delete(state)
            models.storage.save()
            
    return jsonify({}), 200
 