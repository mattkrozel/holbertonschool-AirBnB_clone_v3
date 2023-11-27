#!/usr/bin/python3
'''
places API blueprint module
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_place(city_id=None):
    '''
    gets list of places
    '''
    myCity = storage.get('City', city_id)
    if myCity is None:
        abort(404)
    myPlaces = myCity.places
    myPlaces = [place.to_dict() for place in myPlaces]
    return (jsonify(myPlaces), 200)


@app_views.route('/places/place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    '''
    gets list of places
    '''
    my_places = storage.get('Place', place_id)
    if my_places is None:
        abort(404)
    return (jsonify(my_places.to_dict()), 200)




@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    deletes place based off id
    '''
    place_d = storage.get('Place', place_id)
    if place_d is None:
        abort(404)
    place_d.delete()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def make_place(city_id):
    '''
    creates new place
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    myCity = data.get('City', city_id)
    if myCity is None:
        abort(404)
    userId = data.get('user_id')
    if userId is None:
        return (jsonify({'error': 'Missing user_id'}), 400)
    new_user = data.get('user', userId)
    if new_user is None:
        abort(404)
    name = data.get('name')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    new_place = Place()
    new_place.city_id = myCity.id
    for key, val in data.items():
        setattr(new_place, key, val)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    '''
    updates specific state
    '''
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    info = storage.get_json()
    if info is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    disallowed = ['id', 'user_id', 'city_id', 'created_at',
                  'updated_at']
    for key, value in info.items():
        if key not in disallowed:
            setattr(places, key, value)
    places.save()
    return jsonify(places.to_dict(), 200)
