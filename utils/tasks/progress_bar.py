import time
from tqdm import tqdm, tqdm_notebook
# from progressbar import AdaptiveETA, Bar, Percentage, ProgressBar, SimpleProgress, Timer


# class ProgressBar:
#     def __init__(self, n):
#         self.pbar = ProgressBar(widgets=[Percentage(), ' (', SimpleProgress(), ')', Bar(), Timer(), ' '],
#                                 redirect_stdout=True)
#         self.i = 0
#         self.pbar.start(max_value=n)
#
#     def update(self, n=1):
#         self.i += n
#         self.pbar.update(self.i)
#
#     def finish(self):
#         self.pbar.finish()


class ProgressBar(object):
    def __init__(self, n, ipython_notebook=False):
        self.n = n
        if ipython_notebook is not False:
            self.pbar = tqdm_notebook(total=n)
        else:
            self.pbar = tqdm(total=n)
        self.i = 0
        self.start_time = time.time()

    def update(self, n=1):
        self.i += n
        if self.i <= self.n:
            self.pbar.update(n)

    def write(self, str):
        self.pbar.write(str)

    def finish(self):
        self.write('Completed %d tasks in %f seconds' % (self.i, time.time() - self.start_time))
        self.pbar.close()
