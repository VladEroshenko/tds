import threading
from typing import Callable
import time


def repeat_with_interval(func: Callable[[], None], num_times: int, interval: int):
    """Repeats func num_times with given interval."""

    def _repeat():
        for i in range(num_times):
            func()
            time.sleep(interval)

    t = threading.Thread(target=_repeat)
    t.start()
    return t