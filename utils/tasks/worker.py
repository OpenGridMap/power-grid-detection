import multiprocessing


class Worker(multiprocessing.Process):
    def __init__(self, task_queue, pbar=None):
        super(Worker, self).__init__()
        self.task_queue = task_queue
        self.pbar = pbar

    def run(self):
        while True:
            next_task = self.task_queue.get()

            if next_task is None:
                self.task_queue.task_done()
                break

            next_task()
            self.task_queue.task_done()

            if self.pbar is not None:
                self.pbar.update()

        return
