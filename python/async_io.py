import asyncio
import io

import aiofiles
from PIL import Image

read_times = 300

async def count():
    async with aiofiles.open('1.png', mode='rb') as f:
        raw_data = await f.read()
        # image = Image.open(io.BytesIO(raw_data))
    # with open('1.png', mode='rb') as f:
    #     raw_data = f.read()
    #     image = Image.open(io.BytesIO(raw_data))


async def main():
    c = [count() for _ in range(read_times)]
    await asyncio.gather(*c)


def test_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main()]))
    loop.close()


def test_sync():
    for _ in range(read_times):
        with open('1.png', mode='rb') as f:
            raw_data = f.read()
            # image = Image.open(io.BytesIO(raw_data))


if __name__ == "__main__":
    import time

    s = time.perf_counter()

    # test_sync()
    test_async()

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
