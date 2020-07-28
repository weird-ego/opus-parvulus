from random import randint
import queue

from uploader import Uploader


files = [
    ''.join(chr(randint(65, 65 + 26 - 1)) for _ in range(randint(1, 10)))
    for _ in range(20)
]

print(*files)

q = queue.Queue()
uploader = Uploader(files, 6, q)
uploader.start()

while uploader.is_active():
    progress = q.get()
    print(progress.done, progress.error, progress.total)
