import os
import sublime

from unittesting import DeferrableTestCase

class TestNodeTools(DeferrableTestCase):

    def setUp(self):
        self.test_path = os.path.join(os.path.dirname(__file__), 'data')
        self.test_js_logging_file = os.path.join(self.test_path, 'test_logging.js')
        self.view = sublime.active_window().open_file(self.test_js_logging_file)
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().run_command("close_file")

    def testNodeBuildDocsCommand(self):
        sublime.set_timeout(lambda: self.view.run_command('node_builddocs'), 1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find('Building ...', 0, sublime.IGNORECASE).size(), 0)
        self.assertNotEqual(out_panel.find('Done!', 0, sublime.IGNORECASE).size(), 0)

    def testNodeUglifyCommand(self):
        sublime.set_timeout(lambda: self.view.run_command('node_uglify'), 1000)
        yield 5000
        out_panel = sublime.active_window().find_output_panel('nodejs')
        self.assertNotEqual(out_panel.find(
            'var logMsg="Hello, World!",var1,var2,', 0, sublime.IGNORECASE).size(), 0)
