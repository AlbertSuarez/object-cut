import unittest

from src import ERROR_CODES


class BaseTestClass(unittest.TestCase):

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
        pass

    def check_error(self, response):
        self.assertTrue(response['error'])
        self.assertEqual(ERROR_CODES[response['error_id']], response['message'])

    def check_status_code(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)
