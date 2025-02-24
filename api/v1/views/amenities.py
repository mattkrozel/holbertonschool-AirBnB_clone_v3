#!/usr/bin/python3
'''
amenities API blueprint module
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    '''
    gets list of amenities
    '''
    if amenity_id is None:
        amenity = storage.all('Amenity')
        amenities = [value.to_dict() for key, value in amenity.items()]
        return jsonify(amenities)
    amenities = storage.get('Amenity', amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''
    deletes amenity based off id
    '''
    amenity_d = storage.get('Amenity', amenity_id)
    if amenity_d is None:
        abort(404)
    amenity_d.delete()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def make_amenity():
    '''
    creates new amenity
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    name = data.get('name')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity()
    new_amenity.name = name
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
    updates specific amenity
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    disallowed = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in disallowed:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict(), 200)
