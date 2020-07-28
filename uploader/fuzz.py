from random import randint
import queue
from time import sleep

from uploader import Uploader, Worker


files = [
    ''.join(chr(randint(65, 65 + 26 - 1)) for _ in range(randint(1, 10)))
    for _ in range(20)
]

print(*files)


Worker.upload = lambda self: sleep(randint(0, 100_000) / 100_000)

q = queue.Queue()

max_time = 20 / 3 + 1

for i in range(100):
    with Uploader(files, 3, q) as upload:
        for i, progress in enumerate(upload.iter_progress()):
            print(progress.done, progress.error, progress.total)
