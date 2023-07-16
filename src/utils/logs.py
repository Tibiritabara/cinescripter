import logging

from pythonjsonlogger import jsonlogger

from utils.common import SettingsLoader

APP_NAME = "LOGS"
options = SettingsLoader.load(APP_NAME, {})
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(filename)s %(module)s')
logHandler.setFormatter(formatter)
level = logging.getLevelName(options.get("level", "INFO"))
logHandler.setLevel(int(level))
logger.setLevel(int(level))
logger.addHandler(logHandler)
