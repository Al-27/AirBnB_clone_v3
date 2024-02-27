#!/usr/bin/python3
""" indx """
from api.v1.views import app_views
from flask import jsonify, request
import models

classes = ["BaseModel", "User", "Place", "City", "Amenity", "Review", "State"]

def GetClass(classname):
    """
    return the Class of the specified classname from the module
    """
    import importlib
    module = importlib.import_module(f"models.{'base_model' if classname == 'BaseModel' else classname.lower()}")
    ModelClass = getattr(module, classname)
    return ModelClass

@app_views.route("/")
def home_route():
    return ""

@app_views.route("/status",strict_slashes=False)
def status_route():
    obj = {"status": "OK"}
    return jsonify(obj)
    

@app_views.route("/stats", strict_slashes=False)
def stats_route():
    stats = {}
    for clas in classes:
        stats[clas] = models.storage.count(GetClass(clas))
    return jsonify(stats)
    