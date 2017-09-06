import os
import datetime
import logging

from .nodejs_constants import PLUGIN_DEBUG_FILE

PLUGIN_STR  = 'Nodejs Plugin'
DEBUG_LEVEL = 'DEBUG'
INFO_LEVEL  = 'INFO'


def cur_time():
    return datetime.datetime.now().isoformat()

# global debug function
def debug(key, value):
    is_debug = True if os.path.exists(PLUGIN_DEBUG_FILE) else False
    if is_debug:
        print("{0} - {1} - {2} => {3} - {4}".format(PLUGIN_STR, 
                                            DEBUG_LEVEL, cur_time(), key, value))

def info(msg):
    print("{0} - {1} - {2} => {3}".format(PLUGIN_STR, INFO_LEVEL, cur_time(), msg))