import os

from .nodejs_base import *
from .nodejs_constants import PLUGIN_PATH, BUILDER_PATH, UGLIFY_PATH
from .nodejs_debug import debug
# Commands to run


class NodeScratchOutput(NodeTextCommand):

    def run(self, edit, **kwargs):
        if kwargs['clear']:
            region = sublime.Region(0, self.active_view().size())
            self.active_view().erase(edit, region)
        self.active_view().insert(edit, 0, kwargs['output'])


class NodeBuilddocsCommand(NodeTextCommand):
    """
    Command to build docs
    """

    def run(self, edit):
        doc_builder = os.path.join(PLUGIN_PATH, BUILDER_PATH)
        command = ['node', doc_builder]
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)


class NodeRunCommand(NodeTextCommand):
    """
    Command to Run node
    """

    def run(self, edit):
        command = """kill -9 `ps -ef | grep node | grep -v grep | awk '{print $2}'`"""
        os.system(command)
        command = ['node', self.view.file_name()]
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)


class NodeDrunCommand(NodeTextCommand):
    """
    Command to run node with debug
    """

    def run(self, edit):
        cmd = """kill -9 `ps -ef | grep node | grep -v grep | awk '{print $2}'`"""
        os.system(cmd)

        cmd = ['node', '--version']
        version = self.run_os_command(cmd).decode()

        if version.startswith("v6"):
            command = ['node', 'debug', self.view.file_name()]
        else:
            command = ['node', '--inspect', '--inspect-port=60123', self.view.file_name()]
            
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)


class NodeRunArgumentsCommand(NodeTextCommand):
    """
    Command to run node with arguments
    """

    def on_input(self, message):
        command = message.split()
        command.insert(0, self.view.file_name())
        command.insert(0, 'node')
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)


class NodeDrunArgumentsCommand(NodeTextCommand):
    """
    RCommand to run node with debug and arguments
    """

    def on_input(self, message):
        command = message.split()
        command.insert(0, self.view.file_name())

        cmd = ['node', '--version']
        version = self.run_os_command(cmd).decode()

        if version.startswith("v6"):
            command.insert(0, 'debug')
        else:
            command.insert(0, '--inspect-port=60123')
            command.insert(0, '--inspect')
            
        command.insert(0, 'node')
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)


class NodeNpmCommand(NodeTextCommand):

    def on_input(self, message):
        command = message.split()
        command.insert(0, "npm")
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmInstallCommand(NodeTextCommand):

    def run(self, edit):
        self.run_command(['npm', 'install'], self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmUninstallCommand(NodeTextCommand):

    def run(self, edit, user_input=None):
        if user_input:
            self.on_input(user_input)
        else:
            self._input_panel = self.get_window().show_input_panel(
                "Package", "", self.on_input, None, None)

    def on_input(self, message):
        command = message.split()
        command.insert(0, "npm")
        command.insert(1, "uninstall")
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmSearchCommand(NodeTextCommand):

    def run(self, edit, user_input=None):
        if user_input:
            self.on_input(user_input)
        else:
            self._input_panel = self.get_window().show_input_panel(
                "Term", "", self.on_input, None, None)

    def on_input(self, message):
        command = message.split()
        command.insert(0, "npm")
        command.insert(1, "search")
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmPublishCommand(NodeTextCommand):

    def run(self, edit):
        self.run_command(['npm', 'publish'], self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmUpdateCommand(NodeTextCommand):

    def run(self, edit):
        self.run_command(['npm', 'update'], self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeNpmListCommand(NodeTextCommand):

    def run(self, edit):
        self.run_command(['npm', 'ls'], self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/Text/Plain text.tmLanguage")
        else:
            self.panel(result)


class NodeUglifyCommand(NodeTextCommand):

    def run(self, edit):
        uglify = os.path.join(PLUGIN_PATH, UGLIFY_PATH)
        command = ['node', uglify, '-i', self.view.file_name()]
        self.run_command(command, self.command_done)

    def command_done(self, result):
        s = sublime.load_settings("Nodejs.sublime-settings")
        if s.get('output_to_new_tab'):
            self.scratch(result, title="Node Output",
                         syntax="Packages/JavaScript/JavaScript.tmLanguage")
        else:
            self.panel(result)
