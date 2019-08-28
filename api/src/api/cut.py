from flask import request, jsonify

from src import *
from src.helper.response_maker import make_response


def post():
    body = request.json

    required_parameters = ['objects']
    if not all(x in body for x in required_parameters):
        return jsonify(make_response(True, message=f'{required_parameters} body parameters are required.')), 400

    if not all(o in COCO_INSTANCE_CATEGORY_NAMES for o in body['objects']):
        return jsonify(make_response(True, message='One or more objects from the list will not be detected.')), 400

    if bool('image_url' in body) == bool('image_base64' in body):
        return jsonify(make_response(True, message='image_url (x)or image_base64 has to be specified')), 400

    return jsonify(make_response(False, image_base64='This will be an image.')), 200
