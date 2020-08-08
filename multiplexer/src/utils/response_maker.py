from flask import jsonify

from src import ERROR_CODES, ERROR_CODES_DEFAULT


def make_response(correlation_id, error, error_id=None, image_url=None, image_base64=None):
    """
    Generates the ObjectCut JSON response.
    :param error: True if the response has to be flagged as error, False otherwise.
    :param error_id: Error message if the request was unsuccessful.
    :param correlation_id: Unique identifier for specific request.
    :param image_url: Image URL pointing to the image result.
    :param image_base64: Image result encoded in base64 if it is a success response.
    :return: ObjectCut JSON response.
    """
    response = dict(correlation_id=correlation_id, error=error)
    if error:
        assert error_id
        response['error_id'] = error_id
        response['message'] = ERROR_CODES.get(error_id, ERROR_CODES_DEFAULT)
    else:
        assert bool(image_url) != bool(image_base64)
        if image_url:
            response['response'] = dict(image_url=image_url)
        else:
            response['response'] = dict(image_base64=image_base64)
    return jsonify(response), 200
