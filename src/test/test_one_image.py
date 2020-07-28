import time
import base64
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--input_image', type=str)
args = parser.parse_args()

URL = 'http://localhost/predict'

def _call_api(image_file):
	"""
	Processes an image_file through the API. For testing purposes
	:param image_file: The location of the image_file.
	:return: Response of the API
	"""
	with open(image_file, "rb") as img_file:
		img_string = base64.urlsafe_b64encode(img_file.read()).decode('utf-8')
	print(img_string)
	for i in range(0, 3):
		try:
			response = requests.post(
				URL,
				data={
					'img': img_string,
					'remove_white': False
				}
			)
			return response
		except Exception as e:
			if i < 2:
				time.sleep(0.125)
			else:
				print('Image failed, throwing error! [{}] - [{}]'.format(
					e, 'None' if not response else response.status_code)
				)
				print('Image that failed:{}'.format(image_file))
				return [], []


if __name__ == '__main__':
	response = _call_api(args.input_image)
	print(response)
