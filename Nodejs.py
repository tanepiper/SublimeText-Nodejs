import os
import subprocess
import sublime
import sublime_plugin
import functools
import threading

def main_thread(callback, *args, **kwargs):
  # sublime.set_timeout gets used to send things onto the main thread
  # most sublime.[something] calls need to be on the main thread
  sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)

class CommandThread(threading.Thread):
  def __init__(self, command, on_done, working_dir="", fallback_encoding="", env={}):
    threading.Thread.__init__(self)
    self.command = command
    self.on_done = on_done
    self.working_dir = working_dir
    self.fallback_encoding = fallback_encoding
    self.env = os.environ.copy()
    self.env.update(env)

  def run(self):
    try:
      output = subprocess.check_output(self.command)
      main_thread(self.on_done, output)
    except (subprocess.CalledProcessError, e):
      main_thread(self.on_done, e.returncode)
    except (OSError, e):
      if e.errno == 2:
        main_thread(sublime.error_message, "Node binary could not be found in PATH\n\nConsider using the node_command setting for the Node plugin\n\nPATH is: %s" % os.environ['PATH'])
      else:
        raise e


# when sublime loads a plugin it's cd'd into the plugin directory. Thus
# __file__ is useless for my purposes. What I want is "Packages/Git", but
# allowing for the possibility that someone has renamed the file.
# Fun discovery: Sublime on windows still requires posix path separators.
PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '').replace(os.path.sep, '/')

def open_url(url):
  sublime.active_window().run_command('open_url', {"url": url})

def view_contents(view):
  region = sublime.Region(0, view.size())
  return view.substr(region)

def plugin_file(name):
  return os.path.join(PLUGIN_DIRECTORY, name)

class NodeCommand(sublime_plugin.TextCommand):
  def run_command(self, command, callback=None, show_status=True, filter_empty_args=True, **kwargs):
    if filter_empty_args:
      command = [arg for arg in command if arg]

    if 'working_dir' not in kwargs:
      kwargs['working_dir'] = self.get_working_dir()
    s = sublime.load_settings("Nodejs.sublime-settings")

    if s.get('save_first') and self.active_view() and self.active_view().is_dirty():
      self.active_view().run_command('save')

    if command[0] == 'node' and s.get('node_command'):
      command[0] = s.get('node_command')

    if command[0] == 'node' and s.get('node_path'):
      kwargs['env'] = { "NODE_PATH" : str(s.get('node_path')) }

    if command[0] == 'npm' and s.get('npm_command'):
      command[0] = s.get('npm_command')

    if not callback:
      callback = self.generic_done

    thread = CommandThread(command, callback, **kwargs)
    thread.start()

    if show_status:
      message = kwargs.get('status_message', False) or ' '.join(command)
      sublime.status_message(message)

  def generic_done(self, result):
    if not result.strip():
      return
    self.panel(result)


  def _output_to_view(self, output_file, output, clear=False, syntax="Packages/JavaScript/JavaScript.tmLanguage", **kwargs):
      output_file.set_syntax_file(syntax)
      if(clear)

      args = {
          'output': output,
          'clear': clear
      }
      output_file.run_command('nodejs_scratch_output', args)

  def scratch(self, output, title=False, position=None, **kwargs):
      scratch_file = self.get_window().new_file()
      if title:
          scratch_file.set_name(title)
      scratch_file.set_scratch(True)
      self._output_to_view(scratch_file, output, **kwargs)
      scratch_file.set_read_only(True)
      if position:
          sublime.set_timeout(lambda: scratch_file.set_viewport_position(position), 0)
      return scratch_file

  def panel(self, output, **kwargs):
    if not hasattr(self, 'output_view'):
      self.output_view = self.get_window().get_output_panel("nodejs")
    self.output_view.set_read_only(False)
    self._output_to_view(self.output_view, output, clear=True, **kwargs)
    self.output_view.set_read_only(True)
    self.get_window().run_command("show_panel", {"panel": "output.nodejs"})

  def quick_panel(self, *args, **kwargs):
    self.get_window().show_quick_panel(*args, **kwargs)

# A base for all node commands that work with the entire repository
class NodeWindowCommand(NodeCommand, sublime_plugin.WindowCommand):
  def active_view(self):
    return self.window.active_view()

  def _active_file_name(self):
    view = self.active_view()
    if view and view.file_name() and len(view.file_name()) > 0:
      return view.file_name()

  def is_enabled(self):
    return True; # A better test should be made. Fx. is this a js file?


  def get_file_name(self):
    return ''

  # If there is a file in the active view use that file's directory to
  # search for the Git root.  Otherwise, use the only folder that is
  # open.
  def get_working_dir(self):
    file_name = self._active_file_name()
    if file_name:
      return os.path.dirname(file_name)
    else:
      return self.window.folders()[0]

  def get_window(self):
    return self.window

# A base for all node commands that work with the file in the active view
class NodeTextCommand(NodeCommand, sublime_plugin.TextCommand):
  def active_view(self):
    return self.view

  def is_enabled(self):
    return True; # A better test should be made. Fx. is this a js file?

  def get_file_name(self):
    return os.path.basename(self.view.file_name())

  def get_working_dir(self):
    return os.path.dirname(self.view.file_name())

  def get_window(self):
    # Fun discovery: if you switch tabs while a command is working,
    # self.view.window() is None. (Admittedly this is a consequence
    # of my deciding to do async command processing... but, hey,
    # got to live with that now.)
    # I did try tracking the window used at the start of the command
    # and using it instead of view.window() later, but that results
    # panels on a non-visible window, which is especially useless in
    # the case of the quick panel.
    # So, this is not necessarily ideal, but it does work.
    return self.view.window() or sublime.active_window()

# Commands to run


# Command to build docs
class NodeBuilddocsCommand(NodeTextCommand):
  def run(self, edit):
    doc_builder = os.path.join(PLUGIN_PATH, 'tools/default_build.js')
    command = ['node', doc_builder]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")
    else:
      self.panel(result)

# Command to Run node
class NodeRunCommand(NodeTextCommand):
  def run(self, edit):
    command = """kill -9 `ps -ef | grep node | grep -v grep | awk '{print $2}'`"""
    os.system(command)    
    command = ['node', self.view.file_name()]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")
    else:
      self.panel(result)

# Command to run node with debug
class NodeDrunCommand(NodeTextCommand):
  def run(self, edit):
    command = """kill -9 `ps -ef | grep node | grep -v grep | awk '{print $2}'`"""
    os.system(command)
    command = ['node', 'debug', self.view.file_name()]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")
    else:
      self.panel(result)

# Command to run node with arguments
class NodeRunArgumentsCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Arguments", "", self.on_input, None, None)

  def on_input(self, message):
    command = message.split()
    command.insert(0, self.view.file_name());
    command.insert(0, 'node');
    self.run_command(command, self.command_done)

  def command_done(self, result):
    self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")

# Command to run node with debug and arguments
class NodeDrunArgumentsCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Arguments", "", self.on_input, None, None)

  def on_input(self, message):
    command = message.split()
    command.insert(0, self.view.file_name());
    command.insert(0, 'debug');
    command.insert(0, 'node');
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")
    else:
      self.panel(result)

class NodeNpmCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Arguments", "", self.on_input, None, None)

  def on_input(self, message):
    command = message.split()
    command.insert(0, "npm");
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmInstallCommand(NodeTextCommand):
  def run(self, edit):
    self.run_command(['npm', 'install'], self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmUninstallCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Package", "", self.on_input, None, None)

  def on_input(self, message):
    command = message.split()
    command.insert(0, "npm");
    command.insert(1, "uninstall")
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmSearchCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Term", "", self.on_input, None, None)

  def on_input(self, message):
    command = message.split()
    command.insert(0, "npm");
    command.insert(1, "search")
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmPublishCommand(NodeTextCommand):
  def run(self, edit):
    self.run_command(['npm', 'publish'], self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmUpdateCommand(NodeTextCommand):
  def run(self, edit):
    self.run_command(['npm', 'update'], self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeNpmListCommand(NodeTextCommand):
  def run(self, edit):
    self.run_command(['npm', 'ls'], self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/Text/Plain text.tmLanguage")
    else:
      self.panel(result)

class NodeUglifyCommand(NodeTextCommand):
  def run(self, edit):
    uglify = os.path.join(PLUGIN_PATH, 'tools/uglify_js.js')
    command = ['node', uglify, '-i', self.view.file_name()]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    s = sublime.load_settings("Nodejs.sublime-settings")
    if s.get('output_to_new_tab'):
      self.scratch(result, title="Node Output", syntax="Packages/JavaScript/JavaScript.tmLanguage")
    else:
      self.panel(result)
