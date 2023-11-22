#!/usr/bin/python3
"""Returns JSON status"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def json_status():
    return jsonify(status="OK")


@app_views.route('/status', methods=['GET'])
def get_stats():
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
