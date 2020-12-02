from datetime import datetime


def timeit(f):
    def inner(*args, **kwargs):
        start = datetime.now()
        result = f(*args, **kwargs)
        end = datetime.now()

        print(f"{f.__name__} took {(end - start).total_seconds() * 1000}ms")
        return result
    return inner
