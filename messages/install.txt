Nodejs Sublime Text 3 Package
=============================

Overview
--------
The Nodejs Sublime Text 3 Package provides a set of code completion, scripts and tools to work with
[nodejs](http://nodejs.org).

Code Completion
---------------
The package code completion is generated from the main nodejs libraries and global namespaces. To invoke
the code completion start typing the namespace you want (For example, type `fs`) and then Ctrl + Space, you get this:

![A picture of the file system context menu](http://i.imgur.com/ZCFcC.png)

Node Commands
-------------
You can access node commands in two ways.

* Via the menu in `Tools -> Node`
* By accessing the Command Palette and typing `node`

The current commands available are (with Windows binding, other bindings are provided):

* Run current script in node (Alt + R)
* Run current script in node debug (Alt + D)
* Run current script in node and arguments (Ctrl + Alt + r)
* Run current script in node debug and arguments (Ctrl + Alt + D)
* Uglify Code
* NPM Command
* Build documentation (builds the completion files)

Snippets
----------------
Also included are some boilerplate snippets.  They include functionality such as a http server,
reading the contents of a directory, etc.

To access these snippets type `node` in your editor followed by Ctrl + Space

If you have any boilerplate code you would like to see in here, get in touch.

Install
-------
You can install this package from [Sublime Text 3 package manager](https://packagecontrol.io). Also you can install this package manually:

*MacOSX*

    `git clone https://github.com/tanepiper/SublimeText-Nodejs.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Nodejs`

*Windows*

    `git clone https://github.com/tanepiper/SublimeText-Nodejs "%APPDATA%\Sublime Text 3\Packages\Nodejs"`

*Linux*

    `git clone https://github.com/tanepiper/SublimeText-Nodejs $HOME/.config/sublime-text-3/Packages/Nodejs`

Build Systems
-------------
PLEASE NOTE: The build system will be refactored to provide different nodejs build systems (such as jake)

If you have a JavaScript file open, by selecting `Tools -> Build Systems -> Nodejs` and
then hitting Ctrl + B, you will activate the node build system on your file and node will try to run it.
You may need to add a `path` variable to the settings object for this if your node executable is not found

TODO
----
* ~~uglify_js.js and other ./tools/*.js scripts don't work when the package is installed by SublimeText package manager~~
* Refactor plugin's classes inheritance in Nodejs.py
* Generate Sublime Text completions during installation phase depending on the version of installed Node
* Check for nvm installation
* Replace the Nodejs.sublime-build to work with [jake](https://github.com/mde/jake)
* Reorganise menu structure
* Improve code completion snippets where possible
* Provide an interface for writing JavaScript plugins

Author & Contributors
----------------------
The original author of this package [Tane Piper](https://github.com/tanepiper).
At the time the project maintainer is [Vardan Pogosian](https://github.com/varp).
