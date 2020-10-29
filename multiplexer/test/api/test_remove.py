import os

from src.utils import image, env
from test.base import BaseTestClass


class MultiplexerRemoveTest(BaseTestClass):

    def setUp(self):
        self.secret_access = env.get_secret_access()
        self.img_url = 'https://objectcut.com/docs/images/object-cut.png'
        self.img_url_wrong = 'https://example.com/not-existing.jpg'
        self.img_base64_wrong = 'not-a-base64'
        self.img_path = os.path.join('test', 'data', 'person.jpg')

    def test_image_url_background_transparent(self):
        form_data = dict(image_url=self.img_url)
        response = self.hit_remove(form_data, secret_access=self.secret_access)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_success(response.json())

    def test_image_url_foreground_transparent(self):
        form_data = dict(image_url=self.img_url, to_remove='foreground')
        response = self.hit_remove(form_data, secret_access=self.secret_access)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_success(response.json())

    def test_base64_background_white(self):
        image_base64 = image.encode(self.img_path)
        form_data = dict(image_base64=image_base64, output_format='base64', color_removal='white')
        response = self.hit_remove(form_data, secret_access=self.secret_access)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_success(response.json())

    def test_error_unauthorized(self):
        form_data = dict(image_url=self.img_url)
        response = self.hit_remove(form_data)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '003')

    def test_error_wrong_image_url(self):
        form_data = dict(image_url=self.img_url_wrong)
        response = self.hit_remove(form_data, secret_access=self.secret_access)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '002')

    def test_error_wrong_image_base64(self):
        form_data = dict(image_base64=self.img_base64_wrong)
        response = self.hit_remove(form_data, secret_access=self.secret_access)
        self.check_status_code(response)
        self.check_response(response.json())
        self.check_error(response.json(), '002')
