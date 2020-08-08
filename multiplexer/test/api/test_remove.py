import os
import unittest
import requests

from src import SECRET_ACCESS
from src.utils import image


class MultiplexerRemoveTest(unittest.TestCase):

    def setUp(self):
        self.endpoint = 'http://0.0.0.0:80/remove'
        self.headers = {'Host': 'multiplexer', 'X-Secret-Access': SECRET_ACCESS}
        self.img_url = 'https://avatars2.githubusercontent.com/u/15660893?s=460&u=87386c900ffae1e679d806e364d17d3166db6ccb&v=4'
        self.img_folder = os.path.join('..', 'examples')
        self.timeout = 30

    def test_image_url(self):
        json_body = dict(image_url=self.img_url)
        response = requests.post(self.endpoint, json=json_body, headers=self.headers, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertIn('correlation_id', response)
        self.assertIn('error', response)
        self.assertIn('response', response)
        self.assertNotIn('error_id', response)
        self.assertNotIn('message', response)
        self.assertIn('image_url', response['response'])
        self.assertNotIn('image_base64', response['response'])
        self.assertFalse(response['error'])
        self.assertIsNotNone(response['correlation_id'])
        self.assertIsNotNone(response['response'])
        self.assertIsNotNone(response['response']['image_url'])

    def test_base64(self):
        img_files = [os.path.join(self.img_folder, f) for f in os.listdir(self.img_folder)]
        for img in img_files:
            image_base64 = image.encode(img)
            json_body = dict(image_base64=image_base64, output_format='base64', white_background=True)
            response = requests.post(self.endpoint, json=json_body, headers=self.headers, timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            response = response.json()
            self.assertIn('correlation_id', response)
            self.assertIn('error', response)
            self.assertIn('response', response)
            self.assertNotIn('error_id', response)
            self.assertNotIn('message', response)
            self.assertIn('image_base64', response['response'])
            self.assertNotIn('image_url', response['response'])
            self.assertFalse(response['error'])
            self.assertIsNotNone(response['correlation_id'])
            self.assertIsNotNone(response['response'])
            self.assertIsNotNone(response['response']['image_base64'])
            correlation_id = response['correlation_id']
            output_path = os.path.join('test', 'data', '{}.png'.format(correlation_id))
            image.decode(correlation_id, response['response']['image_base64'], output_path=output_path)
