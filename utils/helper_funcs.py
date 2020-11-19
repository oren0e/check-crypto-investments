from functools import wraps

from typing import Callable

from threading import Semaphore, Timer


def ratelimit(limit: int, every: int) -> Callable:
    def limit_decorator(f: Callable) -> Callable:
        semaphore = Semaphore(limit)
        @wraps(f)
        def wrapper(*args, **kwargs):
            semaphore.acquire()
            try:
                return f(*args, **kwargs)
            finally:    # don't catch, but ensure semaphore release
                timer = Timer(every, semaphore.release)     # release the lock every `every` seconds
                timer.setDaemon(True)
                timer.start()
        return wrapper
    return limit_decorator
