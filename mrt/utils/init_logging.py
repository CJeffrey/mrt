import logging


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('mrt.log', mode='w')
    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(filename)s %(message)s')
    fh.setFormatter(log_format)

    logger.addHandler(fh)

    logger.info('setup logger successfully')
