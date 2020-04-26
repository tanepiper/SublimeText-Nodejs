import os

# when sublime loads a plugin it's cd'd into the plugin directory. Thus
# __file__ is useless for my purposes. What I want is "Packages/Git", but
# allowing for the possibility that someone has renamed the file.
PLUGIN_VERSION = '2.0.6'

PLUGIN_PATH = PLUGIN_DIRECTORY = os.path.split(os.path.dirname(__file__))[0]
PLUGIN_LIB_DIR = os.path.join(PLUGIN_PATH, "lib")
PLUGIN_DEBUG_FILE = os.path.join(PLUGIN_PATH, '.debug_plugin')
PLUGIN_PACKAGE_LOCK = os.path.join(PLUGIN_PATH, 'package-lock.json')
UGLIFY_PATH = os.path.join(PLUGIN_PATH, "tools", "uglify_js.js")
BUILDER_PATH = os.path.join(PLUGIN_PATH, "tools", "default_build.js")
