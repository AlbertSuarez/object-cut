def make_response(error, message=None, image_base64=None):
    response = dict(error=error)
    if error:
        response['message'] = message
    else:
        response['response'] = dict(image_base64=image_base64)
    return response
