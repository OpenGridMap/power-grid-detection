import multiprocessing

from utils.tasks.worker import Worker
from utils.progress_bar import PBar


class TasksHandler:
    def __init__(self, tasks, n_workers=None, pbar=True):
        self.task_queue = multiprocessing.JoinableQueue()

        if not pbar:
            self.pbar = None
        else:
            self.pbar = PBar(len(tasks))

        if n_workers is None:
            self.n_workers = multiprocessing.cpu_count() * 2
        else:
            self.n_workers = n_workers

        self.workers = [Worker(self.task_queue, self.pbar) for _ in range(self.n_workers)]

        for w in self.workers:
            w.start()

        self.map(tasks)

    def add_task(self, task):
        self.task_queue.put(task)

    def map(self, tasks):
        for task in tasks:
            self.add_task(task)

        for i in range(self.n_workers):
            self.add_task(None)

    def wait_completion(self):
        self.task_queue.join()

        if self.pbar is not None:
            self.pbar.finish()
