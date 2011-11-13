Nodejs Sublime Text 2 Package
=============================

Overview
---------
This snippet provides a nearly complete set of snippets for the nodejs 0.6.x namespace.

By setting your file type to JavaScript, and selecting `Tools -> Build Systems -> Nodejs` when you
type certain namespaces and then Ctrl + Space, you will get autocomplete suggestions in the context menu.

For example, type `fs` then Ctrl + Space, you get this:

![A picture of the file system context menu](http://i.imgur.com/QLVPt.jpg)

Build Systems
-------------

If you have a JavaScript file open, by selecting selecting `Tools -> Build Systems -> Nodejs` and
then hitting Ctrl + B, you will activate the node build system on your file and node will try to run it.

Currently it does not accept arguments, and you may need to close Sublime Text to end your process if it's
long running - these are currently being looked in to.

Author & Contributors
----------------------
[Tane Piper](http://twitter.com/tanepiper)
