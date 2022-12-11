"""
"""
from time import perf_counter
from typing import Callable, Any


def print_execution_time(func: Callable) -> Callable:
    """
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        return_value =  func(*args, **kwargs)
        run_time = perf_counter() - start_time
        print(f'It took {run_time:.2f} seconds to run.')
        return return_value
    return wrapper