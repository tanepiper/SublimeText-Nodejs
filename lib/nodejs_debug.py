import os
import logging

from .nodejs_constants import PLUGIN_DEBUG_FILE

# global debug function
def debug(key, value):
    is_debug = True if os.path.exists(PLUGIN_DEBUG_FILE) else False   
    if is_debug:
        logging.debug("Nodejs Plugin - {0} {1}".format(key, value))