import commands, re
import sublime, sublime_plugin

class Nodejs(sublime_plugin.TextCommand):
  def run(self, edit):
    v = self.view
    currPos = v.sel()[0].begin()
    currLineRegion = v.line(currPos)

    regx = re.compile(" ")
    output = commands.getoutput("node " + regx.sub("\ ", self.view.file_name()))

    if len(lint) > 0:
      v.insert(edit, 0, output)

class NodejsHintListener(sublime_plugin.EventListener):
  def on_post_save(self, view):
    currPos = v.sel()[0].begin()
    currLineRegion = v.line(currPos)

    regx = re.compile(" ")
    output = commands.getoutput("jshint " + regx.sub("\ ", self.view.file_name()))

    if len(lint) > 0:
      v.insert(edit, 0, output)

