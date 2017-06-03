import os
import sublime

def open_url(url):
  sublime.active_window().run_command('open_url', {"url": url})

def view_contents(view):
  region = sublime.Region(0, view.size())
  return view.substr(region)

def plugin_file(name):
  return os.path.join(PLUGIN_DIRECTORY, name)