import time


# 线程锁装饰器:保证操作的原子性
def synchronized(lock):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def timer():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print('函数%s运行时间为%s' % (func.__name__, end - start))
            return result

        return wrapper

    return decorator
