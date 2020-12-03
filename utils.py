from datetime import datetime
from functools import wraps


def timeit(iterations=1):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            times = []
            result = None

            for i in range(iterations):
                start = datetime.now()
                result = f(*args, **kwargs)
                end = datetime.now()

                delta = (end - start).total_seconds() * 1000
                times.append(delta)

                print(f"Iteration {i+1} took {delta}ms")

            avg = sum(times) / len(times)
            print(f"{f.__name__} took {avg}ms to run on average")

            return result
        return wrapper
    return inner
