import os
import sublime
import sublime_plugin
import threading
import subprocess
import functools
import tempfile

# when sublime loads a plugin it's cd'd into the plugin directory. Thus
# __file__ is useless for my purposes. What I want is "Packages/Git", but
# allowing for the possibility that someone has renamed the file.
# Fun discovery: Sublime on windows still requires posix path separators.
PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')


def main_thread(callback, *args, **kwargs):
    # sublime.set_timeout gets used to send things onto the main thread
    # most sublime.[something] calls need to be on the main thread
    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)


def open_url(url):
    sublime.active_window().run_command('open_url', {"url": url})

def view_contents(view):
    region = sublime.Region(0, view.size())
    return view.substr(region)


def plugin_file(name):
    return os.path.join(PLUGIN_DIRECTORY, name)


def _make_text_safeish(text, fallback_encoding):
    # The unicode decode here is because sublime converts to unicode inside
    # insert in such a way that unknown characters will cause errors, which is
    # distinctly non-ideal... and there's no way to tell what's coming out of
    # git in output. So...
    try:
        unitext = text.decode('utf-8')
    except UnicodeDecodeError:
        unitext = text.decode(fallback_encoding)
    return unitext

class CommandThread(threading.Thread):
  def __init__(self, command, on_done, working_dir="", fallback_encoding=""):
    threading.Thread.__init__(self)
    self.command = command
    self.on_done = on_done
    self.working_dir = working_dir
    self.fallback_encoding = fallback_encoding

  def run(self):
    try:
      # Per http://bugs.python.org/issue8557 shell=True is required to
      # get $PATH on Windows. Yay portable code.
      shell = os.name == 'nt'
      if self.working_dir != "":
        os.chdir(self.working_dir)

        proc = subprocess.Popen(self.command,
          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
          shell=shell, universal_newlines=True)
        output = proc.communicate()[0]
        # if sublime's python gets bumped to 2.7 we can just do:
        # output = subprocess.check_output(self.command)
        main_thread(self.on_done, _make_text_safeish(output, self.fallback_encoding))
    except subprocess.CalledProcessError, e:
      main_thread(self.on_done, e.returncode)
    except OSError, e:
      if e.errno == 2:
        main_thread(sublime.error_message, "Node binary could not be found in PATH\n\nConsider using the node_command setting for the Node plugin\n\nPATH is: %s" % os.environ['PATH'])
      else:
        raise e


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

  def _output_to_view(self, output_file, output, clear=False, syntax="Packages/Diff/Diff.tmLanguage"):
    output_file.set_syntax_file(syntax)
    edit = output_file.begin_edit()
    if clear:
      region = sublime.Region(0, self.output_view.size())
      output_file.erase(edit, region)
    output_file.insert(edit, 0, output)
    output_file.end_edit(edit)

  def scratch(self, output, title=False, **kwargs):
    scratch_file = self.get_window().new_file()
    if title:
      scratch_file.set_name(title)
    scratch_file.set_scratch(True)
    self._output_to_view(scratch_file, output, **kwargs)
    scratch_file.set_read_only(True)
    return scratch_file

  def panel(self, output, **kwargs):
    if not hasattr(self, 'output_view'):
      self.output_view = self.get_window().get_output_panel("git")
    self.output_view.set_read_only(False)
    self._output_to_view(self.output_view, output, clear=True, **kwargs)
    self.output_view.set_read_only(True)
    self.get_window().run_command("show_panel", {"panel": "output.git"})

  def quick_panel(self, *args, **kwargs):
    self.get_window().show_quick_panel(*args, **kwargs)

# A base for all git commands that work with the entire repository
class NodeWindowCommand(NodeCommand, sublime_plugin.WindowCommand):
  def active_view(self):
    return self.window.active_view()

  def _active_file_name(self):
    view = self.active_view()
    if view and view.file_name() and len(view.file_name()) > 0:
      return view.file_name()

  # If there's no active view or the active view is not a file on the
  # filesystem (e.g. a search results view), we can infer the folder
  # that the user intends Git commands to run against when there's only
  # only one.
  def is_enabled(self):
    if self._active_file_name() or len(self.window.folders()) == 1:
      return os.path.realpath(self.get_working_dir())

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

# A base for all git commands that work with the file in the active view
class NodeTextCommand(NodeCommand, sublime_plugin.TextCommand):
  def active_view(self):
    return self.view

  def is_enabled(self):
    # First, is this actually a file on the file system?
    if self.view.file_name() and len(self.view.file_name()) > 0:
      return os.path.realpath(self.get_working_dir())

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

class NodeRunCommand(NodeTextCommand):
  def run(self, edit):
    command = ['node', self.view.file_name()]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    self.scratch(result, title="Node Output", syntax=plugin_file("JavaScript.tmLanguage"))

class NodeRunArgumentsCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Arguments", "", self.on_input, None, None)

  def on_input(self, message):
    command = ['node', self.view.file_name(), message]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    self.scratch(result, title="Node Output", syntax=plugin_file("JavaScript.tmLanguage"))

class NodeNpmCommand(NodeTextCommand):
  def run(self, edit):
    self.get_window().show_input_panel("Arguments", "", self.on_input, None, None)

  def on_input(self, message):
    command = ['npm', message, self.get_working_dir()]
    self.run_command(command, self.command_done)

  def command_done(self, result):
    self.scratch(result, title="NPM Output", syntax=plugin_file("JavaScript.tmLanguage"))