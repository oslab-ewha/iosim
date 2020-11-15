import logging

def init(prog):
    global      logger

    # 
    log_path = None
    level = logging.INFO

    logger = logging.getLogger(prog)
    if log_path != None:
        handler = logging.FileHandler(filename=log_path)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s', datefmt="%m/%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)

def info(str):
    global      logger
    logger.info(str)

def debug(str):
    global      logger
    logger.debug(str)

def warn(str):
    global      logger
    logger.warn(str)

def error(str):
    global      logger
    logger.error(str)
