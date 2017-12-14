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

        version = self.node_version()
        debug('node_version', version)

        if version == 6:
            command = ['node', '--inspect=localhost:60123',
                                        '--debug-brk', self.view.file_name()]
        if version > 6:
            command = ['node', '--inspect-brk=localhost:60123', self.view.file_name()]
            
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
    Command to run node with debug and arguments
    """

    def on_input(self, message):
        self._kill_node_processes()
        
        command = message.split()
        command.insert(0, self.view.file_name())

        version = self.node_version()
        debug('node_version', version)

        if version == 6:
            command.insert(0, '--debug-brk')
            command.insert(0, '--inspect=localhost:60123')
        if version > 6:
            command.insert(0, '--inspect-brk=localhost:60123')
            
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
