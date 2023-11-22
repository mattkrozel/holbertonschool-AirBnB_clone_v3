#!/usr/bin/python3
'''
state blueprint
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import State, storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    '''
    gets list of states
    '''
    if state_id is None:
        state = storage.all('State')
        states = [value.to_dict() for key, value in state.items()]
        return jsonify(states)
    states = storage.get('State', state_id)
    if states is not None:
        return jsonify(states.to_dict())
    abort(404)

@app_views.route('/states/<s_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(s_id):
    '''
    deletes state based off id
    '''
    state_d = storage.get('State', s_id)
    if state_d is None:
        abort(404)
    storage.delete(state_d)
    storage.save()
    return (jsonify({}))

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def make_state():
    '''
    creates state
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'Error': 'Not a JSON'}), 400)
    name = data.get('name')
    if name is None:
        return (jsonify({'error': 'Missing name'}), 400)
    new_state = State(**data)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''
    updates state
    '''
    data = request.get_json()
    if data is None:
        return (jsonify({'Error': 'Not a JSON'}), 400)
    state1 = storage.get('State', state_id)
    if state1 is None:
        abort(404)
    disallowed = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key in disallowed:
            setattr(state1, key, value)
    state1.save()
    return jsonify(state1.to_dict())
