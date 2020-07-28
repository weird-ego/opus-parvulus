from random import randint
from time import sleep
import queue

from uploader import Uploader


files = [
    ''.join(chr(randint(65, 65 + 26 - 1)) for _ in range(randint(1, 10)))
    for _ in range(20)
]

print(*files)

q = queue.Queue()

with Uploader(files, 6, q) as upload:
    for progress in upload.iter_progress():
        print(progress.done, progress.error, progress.total)
        print(upload.estimate())

        upload.interrupt()
        sleep(2)
        upload.resume()
