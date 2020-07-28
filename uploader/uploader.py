from multiprocessing import Queue, Process, Value
from threading import Thread, Lock
import queue
from time import sleep
from signal import SIGSTOP, SIGCONT
import logging
from os import kill
from collections import namedtuple
from time import time


class Worker(Process):

    def __init__(self, from_queue, to_queue):
        super().__init__()
        self.from_queue = from_queue
        self.to_queue = to_queue
        self.current = None

    def sighup_recieved(self, *_):
        logging.info('Worker process recived SIGHUP. This indicates'
                     ' misuse of Uploader instance. You should howsome'
                     ' wait for worker processes to complete. Try '
                     ' Uploader.join() or polling with Uploader.is_alive()'
                     ' or polling result queue.')
        logging.debug('Prematurely terminated due to SIGHUP, while processing'
                      f' {self.current}')

    def upload(self):
        sleep(len(self.current) / 10)
        return self.current

    def _upload(self):
        logging.debug(f'Process(pid={self.pid}) started upload'
                      ' of {self.current}')
        value = self.upload()
        self.to_queue.put((value, None), block=True)
        logging.debug(f'Process(pid={self.pid}) finished upload'
                      ' of {self.current}')

    def run(self):
        while not self.from_queue.empty():
            try:
                self.current = self.from_queue.get(block=True, timeout=10)
            except queue.Empty:
                exit()

            try:
                self._upload()
            except Exception as e:
                logging.error(f'Process(pid={self.pid}) recieved {e}'
                              f' while uploading {self.current}')
                self.to_queue.put((self.current, e), block=True)
        self.to_queue.close()


Progress = namedtuple('Progress', ('done', 'error', 'total'))


class BaseWriter:
    def __init__(self, from_queue, to_queue, amount):
        super().__init__()
        self._from_queue = from_queue
        self._to_queue = to_queue
        self._amount = amount
        self._done = 0
        self._error = 0
        self._total = 0
        self.last = None
        self.times = []

    def estimate(self, n_workers):
        if self.times:
            return (sum(self.times) / len(self.times)) \
                   * self.amount / n_workers
        else:
            return float('nan')

    def run(self):
        while self.amount > 0:
            try:
                item, ex = self._from_queue.get(block=True, timeout=10)
            except queue.Empty:
                continue
            if ex:
                self._error += 1
            else:
                now = time()
                if self.last is not None:
                    diff = now - self.last
                    self.times.append(diff)
                self.last = now
                self._done += 1
            self._total += 1
            progress = Progress(
                self._done,
                self._error,
                self._total
            )
            self._to_queue.put(progress, block=True)
            self.amount -= 1


class WriterProcessBased(BaseWriter, Process):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._amount = Value('i', self._amount)

    @property
    def amount(self):
        with self._amount.get_lock():
            return self._amount.value

    @amount.setter
    def amount(self, value):
        with self._amount.get_lock():
            self._amount.value = value

    def finish(self):
        self.join()
        self.close()


class WriterThreadBased(BaseWriter, Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = Lock()

    @property
    def amount(self):
        with self.lock:
            return self._amount

    @amount.setter
    def amount(self, value):
        with self.lock:
            self._amount = value

    def finish(self):
        self.join()


class Uploader:

    class AlreadyFinished(Exception):
        pass

    def __init__(self, paths, concurrency_factor, progress_queue):
        self.__paths = Queue(maxsize=len(paths))
        self.__concurrency_factor = concurrency_factor
        self.__interqueue = Queue(maxsize=len(paths))
        if isinstance(progress_queue, queue.Queue):
            writer_type = WriterThreadBased
        else:
            writer_type = WriterProcessBased
        self.writer = writer_type(
            self.__interqueue,
            progress_queue,
            len(paths)
        )
        self.progress_queue = progress_queue
        self.workers = []

        for path in paths:
            self.__paths.put(path)

        self.__entered = False

    @property
    def concurrency_factor(self):
        return self.__concurrency_factor

    def estimate(self):
        return self.writer.estimate(self.concurrency_factor)

    def is_active(self):
        if self.writer.is_alive():
            return self.writer.amount > 0
        return False

    def interrupt(self):
        for worker in self.workers:
            kill(worker.pid, SIGSTOP)

    def resume(self):
        for worker in self.workers:
            kill(worker.pid, SIGCONT)

    def stop(self):
        for worker in self.workers:
            worker.terminate()
            for _ in range(10):
                sleep(.1)
                if not worker.is_alive():
                    break
            else:
                logging.error(f'Process(pid={worker.pid}) became zombie')
        self.writer.amount = 0

    def start(self):
        self.workers = [
            Worker(self.__paths, self.__interqueue)
            for _ in range(self.__concurrency_factor)
        ]

        for worker in self.workers:
            worker.start()

        self.writer.start()

    def get(self, timeout=1):
        """
        this method protects user against calling .get on progress queue,
        while uploader is already entered inactive state.
        """
        while True:
            try:
                return self.progress_queue.get(block=True, timeout=timeout)
            except queue.Empty:
                if self.is_active():
                    continue
                elif self.__entered:
                    raise Uploader.AlreadyFinished
                else:
                    return None

    def iter_progress(self):
        return iter(self.get, None)

    def __enter__(self):
        self.__entered = True
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, _):
        self.__entered = False
        if exc_type is KeyboardInterrupt:
            self.stop()
            raise exc_value
        for worker in self.workers:
            worker.join()
            worker.close()
        self.writer.finish()
        return issubclass(exc_type, Uploader.AlreadyFinished)

    def join(self):
        for worker in self.workers:
            worker.join()
        self.writer.join()
