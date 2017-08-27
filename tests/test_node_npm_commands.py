import os
import time

import sublime
from unittesting import DeferrableTestCase

version = sublime.version()

class TestNpmCommand(DeferrableTestCase):
    def setUp(self):
        test_js_logging_file = os.path.join(os.path.dirname(__file__), 'data', 'test_logging.js')
        self.view = sublime.active_window().open_file(test_js_logging_file)
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)
        

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().run_command("close_file")

    def testNpmCommandRun(self):
        yield 1000 # wait for file is to be opened
        sublime.run_command('node_npm', {'user_input': 'version'})
        yield 1000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('sublime-nodejs', 0, sublime.IGNORECASE).size(), 0)

    def testNpmInstallCommandRun(self):
        yield 1000
        sublime.run_command('node_npm_install')
        yield 1000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('npm WARN sublime-nodejs@', 0, 
                                sublime.IGNORECASE).size(), 0)    

    def testNpmListCommandRun(self):
        yield 1000
        sublime.run_command('node_npm_list')
        yield 1000
        # sublime-nodejs@1.5.6
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('sublime-nodejs@1.5.6', 0, 
                                sublime.IGNORECASE).size(), 0)

    def testNpmSearchCommandRun(self):
        yield 1000
        sublime.run_command('node_search', {'user_input': 'test'})
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('=chaijs', 0, 
                                sublime.IGNORECASE).size(), 0)         
