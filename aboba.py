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
    t.start()  # Start background thread
    return t  # Return reference to started thread


# Example usage
print(__name__)
if __name__ == "__main__":
    def hello_world():
        print("Hello world")


    # Repeat 'hello_world' function 3 times with 2 seconds interval
    t = repeat_with_interval(hello_world, 3, 2)
    print("Main thread still running.")
    t.join()  # Wait until repetition finishes before exiting script
    print('End')