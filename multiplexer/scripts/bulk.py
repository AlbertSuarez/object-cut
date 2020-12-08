import argparse
import os
import time
import uuid
import requests

from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm

from src.utils import env, image, log


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    parser.add_argument('output_folder', type=str)
    parser.add_argument('--endpoint', type=str, default='http://0.0.0.0:80/remove')
    parser.add_argument('--concurrency', type=int, default=3)  # Should be the same as the num of inference containers
    parser.add_argument('--timeout', type=int, default=300)
    parser.add_argument('--to_remove', type=str, default='background', choices={'background', 'foreground'})
    parser.add_argument('--color_removal', type=str, default='transparent', choices={'transparent', 'white'})
    parser.add_argument('--cut', type=int, default=0)
    return parser.parse_args()


def _validate(input_folder, output_folder):
    input_file_list = list()
    output_file_list = list()
    assert os.path.isdir(input_folder)  # Be sure that the input folder exists and it's a folder
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if not file_name.startswith('.'):
            file_path = os.path.join(input_folder, file_name)
            if os.path.isfile(file_path) and image.verify(file_path):  # Be sure that it's an image file
                input_file_list.append(file_path)
                output_file_list.append(os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}.png'))
    log.info(f'Images to process: [{len(input_file_list)}]')
    assert input_file_list and len(input_file_list) == len(output_file_list)
    secret_access = env.get_secret_access()
    assert secret_access
    return input_file_list, output_file_list, secret_access


def __process_thread(param_tuple):
    input_path, output_path, endpoint, secret_access, timeout, to_remove, color_removal = param_tuple
    for attempt in range(3):
        try:
            image_base64 = image.encode(input_path)
            headers = {'Host': 'api.objectcut.com', 'X-Secret-Access': secret_access}
            form_data = dict(
                image_base64=image_base64, output_format='base64',
                to_remove=to_remove, color_removal=color_removal
            )
            response = requests.post(endpoint, data=form_data, headers=headers, timeout=timeout).json()
            image.decode(str(uuid.uuid4()), response['response']['image_base64'], output_path=output_path)
            if image.verify(output_path):
                return True
            else:
                os.remove(output_path)
                return False
        except Exception as e:
            time.sleep(5)  # RTD for error scenarios
            if attempt >= 2:
                log.error(f'Error with image [{input_path}]: [{e}]')
    return False


def _process(
        input_file_list, output_file_list, endpoint, secret_access, concurrency, timeout, to_remove, color_removal, cut
):
    param_list = [
        (input_file_list[i], output_file_list[i], endpoint, secret_access, timeout, to_remove, color_removal)
        for i in range(len(input_file_list))
    ]
    if cut > 0:
        param_list = param_list[:cut]
    with ThreadPool(concurrency) as pool:
        amount_processed = sum(tqdm(pool.imap(__process_thread, param_list, 1), total=len(param_list)))
    log.info(f'Images processed: [{amount_processed}]')


def main(input_folder, output_folder, endpoint, concurrency, timeout, to_remove, color_removal, cut):
    input_file_list, output_file_list, secret_access = _validate(input_folder, output_folder)
    _process(
        input_file_list, output_file_list, endpoint, secret_access, concurrency, timeout, to_remove, color_removal, cut
    )


if __name__ == '__main__':
    args = parse_args()
    main(
        args.input_folder, args.output_folder, args.endpoint, args.concurrency, args.timeout,
        args.to_remove, args.color_removal, args.cut
    )
