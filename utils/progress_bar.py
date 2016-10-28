from progressbar import AdaptiveETA, Bar, Percentage, ProgressBar, SimpleProgress, Timer


class PBar:
    def __init__(self, n):
        self.pbar = ProgressBar(widgets=[Percentage(), ' (', SimpleProgress(), ')', Bar(), Timer(), ' '],
                                redirect_stdout=True)
        self.i = 0
        self.pbar.start(max_value=n)

    def update(self, n=1):
        self.i += n
        self.pbar.update(self.i)

    def finish(self):
        self.pbar.finish()
