import logging
from logging.handlers import RotatingFileHandler


formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
                              '%Y-%m-%d %H:%M:%S')

handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
