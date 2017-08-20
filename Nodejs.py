import os
import sys
import sublime
import sublime_plugin

# when sublime loads a plugin it's cd'd into the plugin directory. Thus
# __file__ is useless for my purposes. What I want is "Packages/Git", but
# allowing for the possibility that someone has renamed the file.
PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '')
PLUGIN_LIB_DIR = os.path.join(PLUGIN_DIRECTORY, "lib")
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '')
UGLIFY_PATH = os.path.join(os.getcwd(), "tools", "uglify_js.js")
BUILDER_PATH = os.path.join(os.getcwd(), "tools", "default_build.js")

# add lib dir to the python's path
sys.path.append(PLUGIN_LIB_DIR)

# import lib's modules
from nodejs_command_thread import *
from nodejs_paths import *
from nodejs_commands import *
