import commands, re
import sublime, sublime_plugin

class Nodejs(sublime_plugin.TextCommand):
  def run(self, edit):
    v = self.view
    currPos = v.sel()[0].begin()
    currLineRegion = v.line(currPos)

    regx = re.compile(" ")
    output = commands.getoutput("node " +
      regx.sub("\ ", self.view.file_name()) +
        " browser:\ true" +
        " es5:\ true" +
        " v8:\ true" +
        " trailing:\ true" +
        " onevar:\ true" +
        " sub:\ true")

    if len(lint) > 0:
      v.insert(edit, 0, output)
