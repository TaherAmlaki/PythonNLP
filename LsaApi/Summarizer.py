from multiprocessing import cpu_count, Pool, Manager
from LsaSummarizer import LsaSummarizer


class SummarizeTexts:
    def __init__(self):
        self._max_workers = cpu_count()
        self._pool = Pool(self._max_workers)
        self._manager = Manager()
        self._result_queue = self._manager.Queue()

    def register_new_request(self, request):
        lsa_summarizer = LsaSummarizer(request)
        self._pool.apply_async(lsa_summarizer.start, (self._result_queue, ))

    @property
    def status(self):
        results = []
        while not self._result_queue.empty():
            results.append(self._result_queue.get())
        return results
