import time
import logging

logger = logging.getLogger(__name__)

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        logger.info(f"{func.__name__} done in {end - start:.2f}s")

        return result
    return wrapper