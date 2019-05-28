import concurrent.futures
import io

import requests
import threading
import time

from PIL import Image


def test_async(times):
    names = ['1.png'] * times
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(load_img, names)


def decode_img(raw_data):
    image = Image.open(io.BytesIO(raw_data))
    gray_image = image.convert('L')



def load_img(name):
    with open(name, mode='rb') as f:
        raw_data = f.read()
        decode_img(raw_data)


def test_sync(times):
    for _ in range(times):
        with open('1.png', mode='rb') as f:
            raw_data = f.read()
            decode_img(raw_data)


if __name__ == "__main__":
    start_time = time.time()

    test_async(30)

    duration = time.time() - start_time
    print(f"Async in {duration} seconds")

    start_time = time.time()

    test_sync(30)

    duration = time.time() - start_time
    print(f"Sync in {duration} seconds")
