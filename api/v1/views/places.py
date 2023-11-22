#!/usr/bin/python3
'''
places API blueprint module
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenities import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/places', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place(city_id=None):
    '''
    gets list of places
    '''
    if city_id is None:
        place = storage.all('Place')
        places = [value.to_dict() for key, value in place.items()]
        return jsonify(places)
    places = storage.get('Place', city_id)
    if places is not None:
        return jsonify(places.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(p_id):
    '''
    deletes place based off id
    '''
    place_d = storage.get('Place', p_id)
    if place_d is None:
        abort(404)
    storage.delete(place_d)
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def make_place():
    '''
    creates new place
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    name = data.get('name')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    new_place = Place(**data)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    updates specific state
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    place = storage.get('State', place_id)
    if place is None:
        abort(404)
    disallowed = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key in disallowed:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict(), 200)
