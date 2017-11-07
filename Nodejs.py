import os
import sys

import shellenv

import sublime
import sublime_plugin


# import lib's modules
from .lib.nodejs_debug import debug, info
from .lib.nodejs_constants import *
from .lib.nodejs_paths import *
from .lib.nodejs_commands import *
from .lib.nodejs_nvm import *


debug('PLUGIN_PATH', PLUGIN_PATH)
debug('PLUGIN_LIB_DIR', PLUGIN_LIB_DIR)
debug('PLUGIN_DEBUG_FILE', PLUGIN_DEBUG_FILE)
debug('UGLIFY_PATH', UGLIFY_PATH)
debug('BUILDER_PATH', BUILDER_PATH)
debug('SHELLENV', shellenv.get_env())


def generate_completions():
    info('Running `node_builddocs` to generate Node.js completions')
    sublime.active_window().run_command('node_builddocs')


def check_and_install_dependencies():
    """
    The function is dosen't check whether npm/node is installed or not.
    """
    # check if already installed
    if os.path.exists(PLUGIN_PACKAGE_LOCK):
        return

    # merge /usr/local/{bin,sbin}
    cmd = ['npm', 'install', '-s']
    exec_options = {
        'quiet': True,
        'working_dir': PLUGIN_PATH
    }

    if os.name != 'nt':
        # update paths for searching executables
        exec_options['cmd'] = cmd
        exec_options['env'] = {}
        exec_options['env'].update({'PATH': shellenv.get_env()[1]['PATH']})
    else:
        exec_options['shell_cmd'] = ' '.join(cmd)

    info('Running `npm install` to install plugin dependencies')

    sublime.active_window().run_command('exec', exec_options)

def create_output_panel():
    view = sublime.active_window().create_output_panel("nodejs")
    view.set_read_only(True)


def plugin_loaded():
    check_and_install_dependencies()
    generate_completions()
    if Nvm.is_installed():
        info('Node.js version from NVM is ' + Nvm.get_current_node_path())


def plugin_unloaded():
    info('Unloaded ' + PLUGIN_VERSION)
