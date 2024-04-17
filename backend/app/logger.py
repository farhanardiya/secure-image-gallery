import logging, os
from logging.handlers import TimedRotatingFileHandler

log_dir = os.path.normpath(os.getcwd())
log_fname = os.path.join(log_dir, 'log/secure_gallery.log')

logger = logging.getLogger('Secure Gallery Logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s %(levelname)s: %(message)s')
logname = (log_fname)
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)
