from functools import wraps
from multiprocessing import cpu_count, Pool, current_process
import time
import logging
from logger_file import get_logger
from concurrent.futures import ProcessPoolExecutor

log = get_logger(__name__)
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def get_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        finish = time.time()
        print(f"time: {finish - start}")
        return result

    return wrapper


@get_time
def factorize(*number):
    """ Синхронна функція """
    name = current_process().name
    logger.debug(f'{name} started...')
    result = []
    for num in number:
        lst = []
        for n in range(1, num + 1):
            # print(n)
            if num % n == 0:
                lst.append(n)
        result.append(lst)
    return result

@get_time
def create_list(num):
    lst = []
    for n in range(1, num + 1):
        if num % n == 0:
            lst.append(n)
    name = current_process().name
    log.info(f"[{name}]: {num}")
    return lst


@get_time
def factorize_mul(*number):
    with Pool(cpu_count()) as p:
        result = p.map(create_list, number)
    return result


if __name__ == "__main__":
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    a1, b1, c1, d1 = factorize_mul(128, 255, 99999, 106510602)
    assert a1 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b1 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c1 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
