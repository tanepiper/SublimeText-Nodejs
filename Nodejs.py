import os
import sys

import sublime
import sublime_plugin


# import lib's modules
from .lib.nodejs_debug import debug, info
from .lib.nodejs_constants import *
from .lib.nodejs_paths import *
from .lib.nodejs_commands import *

debug('PLUGIN_PATH', PLUGIN_PATH)
debug('PLUGIN_LIB_DIR', PLUGIN_LIB_DIR)
debug('PLUGIN_DEBUG_FILE', PLUGIN_DEBUG_FILE)
debug('UGLIFY_PATH', UGLIFY_PATH)
debug('BUILDER_PATH', BUILDER_PATH)


def check_and_install_dependencies():
    """
    The function is dosen't check whether npm/node is installed or not.
    TODO: add check for npm/node existence
    """
    # check if already installed
    if os.path.exists(PLUGIN_PACKAGE_LOCK): return

    # merge /usr/local/{bin,sbin}    
    new_env_path = os.environ['PATH'] + ':/usr/local/bin:/usr/local/sbin'
    
    info('Running `npm install` to install plugin dependencies')

    sublime.active_window().run_command('exec', { 'cmd': ['npm', 'install', '-s'],
                                                'quiet': True,
                                                'working_dir': PLUGIN_PATH,
                                                'env': {'PATH': new_env_path}})

def plugin_loaded():
    info('Loaded ' + PLUGIN_VERSION)
    check_and_install_dependencies()

def plugin_unloaded():
    info('Unloaded ' + PLUGIN_VERSION)