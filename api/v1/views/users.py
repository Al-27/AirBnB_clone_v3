#!/usr/bin/python3
""" usrs """

from api.v1.views import app_views
from flask import jsonify, request, abort
import models


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/users/<user_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def users_route(user_id=None):
    """ str """
    if user_id is None:
        if request.method == "GET":
            users = []
            for user in models.storage.all(models.user.User).values():
                users.append(user.to_dict())
            return jsonify(users)
        else:
            try:
                req = request.get_json()
            except Exception as e:
                abort(400, {"error": "Not a JSON"})

            if "email" not in req.keys():
                abort(400, {"error": "Missing email"})
            if "password" not in req.keys():
                abort(400, {"error": "Missing password"})

            user = models.user.User(**req)
            models.storage.new(user)
            models.storage.save()

            return jsonify(user.to_dict()), 201
    else:
        user_id = f'User.{user_id}'
        user = models.storage.all(models.user.User).get(user_id)

        if user is None:
            abort(404)

        if request.method == "GET":
            return jsonify(user.to_dict())
        elif request.method == "PUT":
            try:
                req = request.get_json()
            except Exception as e:
                abort(400, {"error": "Not a JSON"})

            for k, v in req.items():
                user.__setattr__(k, v)
            user.save()

            return jsonify(user.to_dict()), 200
        else:
            models.storage.delete(user)
            models.storage.save()

    return jsonify({}), 200
