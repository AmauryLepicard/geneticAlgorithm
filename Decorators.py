import datetime


def functionTimer(f):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        f(*args, **kwargs)
        end = datetime.datetime.now()
        print(f.__name__, "executed in ", (end - start).microseconds)

    return wrapper
