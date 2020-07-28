from random import randint
import queue

from uploader import Uploader


files = [
    ''.join(chr(randint(65, 65 + 26 - 1)) for _ in range(randint(1, 10)))
    for _ in range(20)
]

print(*files)

q = queue.Queue()

with Uploader(files, 3, q) as upload:
    for i, progress in enumerate(upload.iter_progress()):
        print(upload.estimate())
        print(progress.done, progress.error, progress.total)
