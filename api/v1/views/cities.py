#!/usr/bin/python3
'''
cities blueprint
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<sid>/cities', methods=['GET'], strict_slashes=False)
def city_state(sid):
    '''
    gets list of cities
    '''
    states = storage.get('State', sid)
    if states is None:
        abort(404)
    cities = states.cities
    final_cities = [city.to_dict() for city in cities]
    return jsonify(final_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    gets city
    '''
    cities = storage.get('City', city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<c_id>', methods=['DELETE'], strict_slashes=False)
def cities(c_id):
    '''
    deletes city based off id
    '''
    city_d = storage.get('City', c_id)
    if city_d is None:
        abort(404)
    storage.delete(city_d)
    return (jsonify({}))


@app_views.route('/states/<id>/cities', methods=['POST'], strict_slashes=False)
def post_city(id):
    '''
    posts specific city
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    name = data.get('name')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    the_state = storage.get('State', id)
    if the_state is None:
        abort(404)
    new_city = City()
    new_city.state_id = id
    new_city.name = name
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    updates specifc city
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city1 = storage.get('State', city_id)
    if city1 is None:
        abort(404)
    disallowed = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in data.items():
        if key not in disallowed:
            setattr(city1, key, value)
    city1.save()
    return jsonify(city1.to_dict())
