from settings import BANANALOG
import logging
from logging import handlers
import os
def log(message):

    # check if file exists
    if not os.path.exists(BANANALOG):
        # create empty log file
        try:
            open(BANANALOG, 'w').close()
        except IOError:
            raise IOError('Unable to create log file %s'%BANANALOG)

    # check if log is writable
    if not os.access(BANANALOG, os.W_OK):
        raise Exception("Log file %s is not writeable."%BANANALOG)

    log = logging.getLogger('bananalog')
    if not log.handlers:
        log.setLevel(logging.DEBUG)
        log_handler = handlers.RotatingFileHandler(BANANALOG)
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        log.addHandler(log_handler)
    log.info(message)
