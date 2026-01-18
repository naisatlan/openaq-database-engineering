import time
from contextlib import contextmanager

@contextmanager
def timer(label, results):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    results[label] = elapsed
