#!/usr/bin/python3
"""Returns JSON status"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def json_status():
    return jsonify(status="OK")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_stats():
    response = {}
    stats = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in stats.items():
        response[value] = storage.count(key)
    return jsonify(response)
