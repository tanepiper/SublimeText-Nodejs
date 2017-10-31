import os
import time

import sublime
from unittesting import DeferrableTestCase

version = sublime.version()


class TestNodeRunArgumentsCommand(DeferrableTestCase):
    def setUp(self):
        test_js_logging_file = os.path.join(os.path.dirname(__file__), 'data', 'test_process.js')
        self.view = sublime.active_window().open_file(test_js_logging_file)
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)
        

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().run_command("close_file")

    def testNodeRunArguments(self):
        sublime.set_timeout(lambda: 
            self.view.run_command('node_run_arguments', {'user_input': '1 2 3'}))
        yield 2000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('The args count is - 5', 0, sublime.IGNORECASE).size(), 0)
