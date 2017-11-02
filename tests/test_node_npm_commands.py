import os
import shutil
import time

import sublime
from unittesting import DeferrableTestCase

version = sublime.version()

class TestNpmCommand(DeferrableTestCase):
    def setUp(self):
        self.test_path = os.path.join(os.path.dirname(__file__), 'data')
        self.test_node_modules_dir = os.path.join(self.test_path, 'node_modules')
        self.test_package_json_file = os.path.join(self.test_path, 'package.json')
        self.test_package_lock_file = os.path.join(self.test_path, 'package-lock.json')
        self.test_js_logging_file = os.path.join(self.test_path, 'test_logging.js')
        self.view = sublime.active_window().open_file(self.test_js_logging_file)
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)
        

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().run_command("close_file")

    def _clear_npm_stuff(self):
        # if files exists remove it before
        if os.path.exists(self.test_node_modules_dir):
            shutil.rmtree(self.test_node_modules_dir)
        if os.path.exists(self.test_package_lock_file):
            os.remove(self.test_package_lock_file)

    def _init_new_package_json_file(self):
        package_json = """
        {
          "name": "test-package",
          "version": "0.0.1",
          "description": "Test node package for the Sublime Text 3 Nodejs Plugin",
          "dependencies": {
            "lorem-ipsum": "=1.0.2"
          }
        }
        """
        if os.path.exists(self.test_package_json_file):
            os.remove(self.test_package_json_file)
        with open(self.test_package_json_file, 'w') as package_file:
            package_file.write(package_json)


    def testNpmCommandRun(self):
        sublime.set_timeout(
            lambda: self.view.run_command('node_npm', {'user_input': 'version'}),
            1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('test-package', 0, sublime.IGNORECASE).size(), 0)

    def testNpmInstallCommandRun(self):
        self._clear_npm_stuff()
        sublime.set_timeout(self.view.run_command('node_npm_install'), 1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('test-package@0.0.1', 0, 
                                sublime.IGNORECASE).size(), 0)    


    def testNpmSearchCommandRun(self):
        sublime.set_timeout(
                self.view.run_command('node_npm_search', {'user_input': 'test'}),
                1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('=chaijs', 0, 
                                sublime.IGNORECASE).size(), 0)     

    def testNpmListCommandRun(self):
        sublime.set_timeout(self.view.run_command('node_npm_list'), 1000)
        yield 5000
        # sublime-nodejs@1.5.6
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('test-package@0.0.1', 0, 
                                sublime.IGNORECASE).size(), 0)

    def testNpmPublishCommandRun(self):
        sublime.set_timeout(lambda: self.view.run_command('node_npm_publish'), 1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('npm ERR!', 0, 
                                sublime.IGNORECASE).size(), 0)

    def testNpmUpdateCommandRun(self):
        self._clear_npm_stuff()
        self._init_new_package_json_file()
        # # first run is installing package lorem-ipsum 1.0.2
        sublime.set_timeout(lambda: self.view.run_command('node_npm_update'), 1000)

        yield 8000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('lorem-ipsum@1.0.2', 0, 
                                sublime.IGNORECASE).size(), 0)