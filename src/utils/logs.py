import os
import logging

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(filename)s %(module)s')
logHandler.setFormatter(formatter)
logHandler.setLevel(int(os.getenv('LOG_LEVEL', logging.DEBUG)))
logger.setLevel(int(os.getenv('LOG_LEVEL', logging.DEBUG)))
logger.addHandler(logHandler)
