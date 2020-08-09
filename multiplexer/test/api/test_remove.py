import os

from src import SECRET_ACCESS
from src.utils import image
from test.base import BaseTestClass


class MultiplexerRemoveTest(BaseTestClass):

    def setUp(self):
        self.img_url = 'https://avatars2.githubusercontent.com/u/15660893?s=460&u=87386c900ffae1e679d806e364d17d3166db6ccb&v=4'
        self.img_url_wrong = 'https://example.com/not-existing.jpg'
        self.img_base64_wrong = 'not-a-base64'
        self.img_folder = os.path.join('..', 'examples')

    def test_image_url(self):
        json_body = dict(image_url=self.img_url)
        response = self.hit_remove(json_body, secret_access=SECRET_ACCESS)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_success(response.json())

    def test_base64(self):
        img_files = [os.path.join(self.img_folder, f) for f in os.listdir(self.img_folder)]
        for img in img_files:
            image_base64 = image.encode(img)
            json_body = dict(image_base64=image_base64, output_format='base64', white_background=True)
            response = self.hit_remove(json_body, secret_access=SECRET_ACCESS)
            self.check_status_code(response)
            self.check_response(response.json())
            self.check_success(response.json())

    def test_error_unauthorized(self):
        json_body = dict(image_url=self.img_url)
        response = self.hit_remove(json_body)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '003')

    def test_error_wrong_image_url(self):
        json_body = dict(image_url=self.img_url_wrong)
        response = self.hit_remove(json_body, secret_access=SECRET_ACCESS)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '002')

    def test_error_wrong_image_base64(self):
        json_body = dict(image_base64=self.img_base64_wrong)
        response = self.hit_remove(json_body, secret_access=SECRET_ACCESS)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '002')
