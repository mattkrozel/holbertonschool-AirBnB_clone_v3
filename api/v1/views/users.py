#!/usr/bin/python3
'''
users API blueprint module
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.users import User
from models import storage

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    '''
    gets list of users
    '''
    if user_id is None:
        user = storage.all('User')
        users = [value.to_dict() for key, value in user.items()]
        return jsonify(users)
    users = storage.get('User', user_id)
    if users is not None:
        return jsonify(users.to_dict(), 200)
    abort(404)


@app_views.route('/users/<user>', methods=['DELETE'], strict_slashes=False)
def delete_user(u_id):
    '''
    deletes user based off id
    '''
    user_d = storage.get('User', u_id)
    if user_d is None:
        abort(404)
    storage.delete(user_d)
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def make_user():
    '''
    creates new user
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    name = data.get('User')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    new_user = User(**data)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    updates specific user
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    disallowed = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key in disallowed:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict(), 200)
