import os
import shutil
import unittest
import requests


class InferencePredictTest(unittest.TestCase):

    def setUp(self):
        self.endpoint = 'http://0.0.0.0:80/predict'
        self.headers = dict(Host='inference')
        self.img_folder = 'examples'
        self.timeout = 30

    def test_all_folder(self):
        img_files = [os.path.join(self.img_folder, f) for f in os.listdir(self.img_folder)]
        for img in img_files:
            img = shutil.copy(img, os.path.join(os.path.sep, 'tmp', os.path.basename(img)))
            response = requests.post(self.endpoint, json=dict(img=img, remove_white=False), headers=self.headers)
            self.assertEqual(response.status_code, 200)
            response = response.json()
            self.assertIn('error', response)
            self.assertIn('message', response)
            self.assertIn('img', response)
            self.assertFalse(response['error'])
            self.assertIsNotNone(response['message'])
            self.assertIsNotNone(response['img'])
            shutil.copy(response['img'], os.path.join('test', 'data', os.path.basename(response['img'])))
