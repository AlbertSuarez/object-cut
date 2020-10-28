import os
import time
import uuid
import requests

from flask import request

from src.utils import image, log, env
from src.utils.response_maker import make_response
from src.utils.timer import Timer


def post():
    """
    Main function for /remove endpoint.
    :return: JSON response.
    """
    correlation_id = str(uuid.uuid4())
    image_path = output_image_path = None
    try:
        body = request.form

        with Timer('Validate input data'):
            if request.headers.get('X-Secret-Access') != env.get_secret_access():
                return make_response(correlation_id, True, error_id='003')

            if bool('image_url' in body) == bool('image_base64' in body):
                return make_response(correlation_id, True, error_id='003')

            output_format = body.get('output_format', 'url')
            to_remove = body.get('to_remove', 'background')
            color_removal = body.get('color_removal', 'transparent')

        with Timer('Download image'):
            if 'image_url' in body:
                image_path = image.download(correlation_id, body['image_url'])
            elif 'image_base64' in body:
                image_path = image.decode(correlation_id, body['image_base64'])
            else:
                image_path = None

            if not image_path:
                return make_response(correlation_id, True, error_id='002')

        with Timer('Hit inference module'):
            json_body = dict(
                img=image_path, to_remove=to_remove, color_removal=color_removal, secret_access=env.get_secret_access()
            )
            request_headers = dict(Host='inference')
            for attempt in range(3):
                try:
                    response = requests.post('http://traefik/predict', json=json_body, headers=request_headers)
                    if response.ok:
                        response = response.json()
                        if not response.get('error'):
                            output_image_path = response.get('img')
                            break
                        else:
                            log.error('Error hitting inference module: [{}]'.format(response.get('message')))
                            raise ValueError
                    else:
                        log.error('Error hitting inference module: Status code [{}]'.format(response.status_code))
                        raise ValueError
                except ValueError:
                    time.sleep(attempt + 1)
                    if attempt >= 2:
                        return make_response(correlation_id, True, error_id='001')

        with Timer('Prepare response'):
            image_url = image_base64 = None
            if output_format == 'url':
                image_url = image.upload(correlation_id, output_image_path)
            else:
                image_base64 = image.encode(output_image_path)
            if not any([image_url, image_base64]):
                return make_response(correlation_id, True, error_id='001')

        return make_response(correlation_id, False, image_url=image_url, image_base64=image_base64)

    except Exception as e:
        log.error('Generic error: [{}]'.format(e))
        log.exception(e)
        return make_response(correlation_id, True, '001')

    finally:
        with Timer('Remove input and output images'):
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            if output_image_path and os.path.exists(output_image_path):
                os.remove(output_image_path)
