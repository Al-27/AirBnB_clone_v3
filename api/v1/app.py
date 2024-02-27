#!/usr/bin/python3
""" app """

from flask import Flask, jsonify
from os import environ as env
import models
from api.v1.views import *

app = Flask(__name__)
app.register_blueprint(app_views)

hst = "0.0.0.0" if env.get(
    "HBNB_API_HOST") is None else env.get("HBNB_API_HOST")
prt = "5000" if env.get("HBNB_API_PORT") is None else env.get("HBNB_API_PORT")


@app.errorhandler(404)
def route_notfound(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def route_error400(e):
    return jsonify(e.description), 400


@app.teardown_appcontext
def teardown(s):
    models.storage.close()


if __name__ == "__main__":
    app.run(host=hst, port=prt)
