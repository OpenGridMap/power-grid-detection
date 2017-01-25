from __future__ import print_function
import multiprocessing
import os

from utils.tasks.progress_bar import ProgressBar
from utils.tasks.worker import Worker

from tqdm import tqdm, tqdm_notebook


class TasksHandler:
    def __init__(self):
        pass

    @staticmethod
    def map(tasks, n_tasks=None, n_workers=None, ipython_notebook=False, **kwargs):
        results = []

        try:
            tasks_queue = multiprocessing.Queue()
            results_queue = multiprocessing.Queue()
            pbar = ProgressBar(n_tasks, ipython_notebook)

            if n_tasks is None:
                if type(tasks) is list:
                    n_tasks = len(tasks)
                else:
                    raise (TypeError, "Expected list received %s " % type(tasks))

            if n_workers is None:
                n_workers = multiprocessing.cpu_count() * 4

            pbar.write('Creating %d workers' % n_workers)
            workers = [Worker(tasks_queue, results_queue, **kwargs) for _ in range(n_workers)]

            for w in workers:
                w.start()

            for task in tasks:
                tasks_queue.put(task)
                # pbar.update()

            for w in range(n_workers):
                tasks_queue.put(None)

            for res in range(n_tasks):
                result = results_queue.get()
                if result is not None:
                    results.append(result)
                pbar.update()

            pbar.write('Joining...')
            for w in workers:
                w.join()

            pbar.finish()
        except KeyboardInterrupt:
            os._exit(1)
        except Exception as e:
            print(e)
            raise e
        finally:
            return results


# class TasksHandler:
#     def __init__(self, tasks, n_workers=None, pbar=True, **kwargs):
#         self.task_queue = multiprocessing.JoinableQueue()
#
#         if not pbar:
#             self.pbar = None
#         else:
#             self.pbar = PBar(len(tasks))
#
#         if n_workers is None:
#             self.n_workers = multiprocessing.cpu_count() * 2
#         else:
#             self.n_workers = n_workers
#
#         self.workers = [Worker(task_queue=self.task_queue, pbar=self.pbar, **kwargs) for _ in range(self.n_workers)]
#
#         for w in self.workers:
#             w.start()
#
#         self.map(tasks)
#
#     def add_task(self, task):
#         self.task_queue.put(task)
#
#     def map(self, tasks):
#         for task in tasks:
#             self.add_task(task)
#
#         for i in range(self.n_workers):
#             self.add_task(None)
#
#     def wait_completion(self):
#         self.task_queue.join()
#
#         if self.pbar is not None:
#             self.pbar.finish()


class TasksPoolHandler:
    def __init__(self, n_workers=None, pbar=True, ipython_notbook=False):
        if n_workers is None:
            n_workers = multiprocessing.cpu_count() * 4

        self.pool = multiprocessing.Pool(processes=n_workers)

        if pbar:
            if not ipython_notbook:
                self.pbar = tqdm
            else:
                self.pbar = tqdm_notebook
        else:
            self.pbar = None

    def map(self, task, args):
        results = []
        total = len(args)
        iterator = self.pool.map(task, args)

        if self.pbar is not None:
            iterator = self.pbar(iterator, total=total)

        for result in iterator:
            results.append(result)

        return results

    def close(self):
        self.pool.close()

    def join(self):
        self.pool.join()

    def __del__(self):
        self.close()
        self.join()
