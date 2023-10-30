#!/usr/bin/python3
'''
Create view for Amenity objects - handles all default RESTful API action
'''

# Import necessary modules
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all Amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''Retrieve list of all Amenity objects'''
    # Get all Amenity objects from the storage
    amenities = storage.all(Amenity).values()
    # Convert objects to dictionaries and jsonify the list
    return jsonify([amenity.to_dict() for amenity in amenities])


# Route for retrieving specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''Retrieve Amenity object'''
    # Get Amenity object with given ID from storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return Amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # Return 404 error if Amenity object is not found
        abort(404)


# Route for deleting specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    # Get Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Delete Amenity object from storage and save changes
        storage.delete(amenity)
        storage.save()
        # Return empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if Amenity object is not found
        abort(404)


# Route for creating new Amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates Amenity object'''
    if not request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error if 'name' key is missing in JSON data
        abort(400, 'Missing name')

    # Create new Amenity object with JSON data
    amenity = Amenity(**data)
    # Save Amenity object to storage
    amenity.save()
    # Return newly created Amenity
    #   object in JSON format with 201 status code
    return jsonify(amenity.to_dict()), 201


# Route for updating an existing Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Update Amenity object'''
    # Get the Amenity object with the given ID from the storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return 400 error if the request data is not in JSON format
        if not request.get_json():
            abort(400, 'Not a JSON')

        # Get JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update attributes of the Amenity object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        # Save updated Amenity object to the storage
        amenity.save()
        # Return updated Amenity object in JSON format with 200 status code
        return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if the Amenity object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''Returns 404: Not Found'''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''Return Bad Request message for illegal request to API.'''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
