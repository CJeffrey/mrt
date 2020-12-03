import functools
import logging

logger = logging.getLogger()


def init_logging():
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('mrt.log', mode='w')
    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(filename)s %(message)s')
    fh.setFormatter(log_format)

    logger.addHandler(fh)

    logger.info('setup logger successfully')


def do_logging(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        logger.debug('enter {}'.format(func.__name__))
        res = func(*args, **kwargs)
        logger.debug('exit {}'.format(func.__name__))
        return res

    return wrap
