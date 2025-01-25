import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        diff_time = end_time - start_time

        diff_hours = int(diff_time // 3600)
        diff_minutes = int((diff_time % 3600) // 60)
        diff_seconds = int((diff_time % 3600) % 60)
        
        print(f"Время выполнения функции {func.__name__}: {diff_hours} ч {diff_minutes} мин {diff_seconds} сек.")
        return result
    return wrapper
