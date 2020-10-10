import os
import unittest
import requests

from src import ERROR_CODES
from src.utils import image
from src.utils.timer import Timer


class BaseTestClass(unittest.TestCase):

    endpoint = 'http://0.0.0.0:80/remove'
    headers = dict(Host='api.objectcut.com')
    timeout = 60

    def hit_remove(self, json_body, secret_access=None):
        self.headers['X-Secret-Access'] = secret_access
        with Timer('/remove'):
            response = requests.post(self.endpoint, data=json_body, headers=self.headers, timeout=self.timeout)
        return response

    def check_response(self, response):
        self.assertIn('correlation_id', response)
        self.assertIn('error', response)
        self.assertIsInstance(response['correlation_id'], str)
        self.assertIsInstance(response['error'], bool)
        if response['error']:
            self.assertIn('error_id', response)
            self.assertIn('message', response)
            self.assertNotIn('response', response)
            self.assertIsInstance(response['error_id'], str)
            self.assertIsInstance(response['message'], str)
            self.assertIn(response['error_id'], ERROR_CODES)
        else:
            self.assertNotIn('error_id', response)
            self.assertNotIn('message', response)
            self.assertIn('response', response)
            self.assertIsInstance(response['response'], dict)
            self.assertNotEqual('image_url' in response['response'], 'image_base64' in response['response'])
            if 'image_url' in response['response']:
                self.assertIsInstance(response['response']['image_url'], str)
            else:
                self.assertIsInstance(response['response']['image_base64'], str)

    def check_success(self, response):
        self.assertFalse(response['error'])
        if 'image_url' in response['response']:
            self.assertIsNotNone(response['response']['image_url'])
            self.assertTrue(requests.get(response['response']['image_url']).ok)
        else:
            correlation_id = response['correlation_id']
            output_path = os.path.join('test', 'data', '{}.png'.format(correlation_id))
            image.decode(correlation_id, response['response']['image_base64'], output_path=output_path)
            image.verify(output_path)

    def check_error(self, response, error_id):
        self.assertTrue(response['error'])
        self.assertEqual(response['error_id'], error_id)
        self.assertEqual(ERROR_CODES[response['error_id']], response['message'])

    def check_status_code(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)
