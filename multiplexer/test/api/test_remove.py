import os
import requests

from src import SECRET_ACCESS
from src.utils import image
from test.base import BaseTestClass


class MultiplexerRemoveTest(BaseTestClass):

    def setUp(self):
        self.endpoint = 'http://0.0.0.0:80/remove'
        self.headers = {'Host': 'multiplexer', 'X-Secret-Access': SECRET_ACCESS}
        self.img_url = 'https://avatars2.githubusercontent.com/u/15660893?s=460&u=87386c900ffae1e679d806e364d17d3166db6ccb&v=4'
        self.img_folder = os.path.join('..', 'examples')
        self.timeout = 30

    def test_image_url(self):
        json_body = dict(image_url=self.img_url)
        response = requests.post(self.endpoint, json=json_body, headers=self.headers, timeout=self.timeout)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_success(response.json())

    def test_base64(self):
        img_files = [os.path.join(self.img_folder, f) for f in os.listdir(self.img_folder)]
        for img in img_files:
            # Prepare request and validate response
            image_base64 = image.encode(img)
            json_body = dict(image_base64=image_base64, output_format='base64', white_background=True)
            response = requests.post(self.endpoint, json=json_body, headers=self.headers, timeout=self.timeout)
            self.check_status_code(response)
            self.check_response(response.json())
            self.check_success(response.json())

            # Post validation for moving result to test/data folder
            response = response.json()
            correlation_id = response['correlation_id']
            output_path = os.path.join('test', 'data', '{}.png'.format(correlation_id))
            image.decode(correlation_id, response['response']['image_base64'], output_path=output_path)
