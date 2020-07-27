
def make_response(error, message=None, image_base64=None):
    """
    Generates the Engine  JSON response.
    :param error: True if the response has to be flagged as error, False otherwise.
    :param message: Message to return if it is a error response.
    :param image_base64: Image result encoded in base64 if it is a success response.
    :return: ObjectCut JSON response.
    """
    response = dict(error=error)
    if error:
        response['message'] = message
    else:
        response['response'] = dict(image_base64=image_base64)
    return response

