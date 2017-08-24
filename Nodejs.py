import os
import sys
import logging

import sublime
import sublime_plugin

# debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# import lib's modules
from .lib.nodejs_debug import debug
from .lib.nodejs_constants import *
from .lib.nodejs_paths import *
from .lib.nodejs_commands import *

debug('PLUGIN_PATH', PLUGIN_PATH)
debug('PLUGIN_LIB_DIR', PLUGIN_LIB_DIR)
debug('PLUGIN_DEBUG_FILE', PLUGIN_DEBUG_FILE)
debug('UGLIFY_PATH', UGLIFY_PATH)
debug('BUILDER_PATH', BUILDER_PATH)
