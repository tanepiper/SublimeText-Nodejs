Nodejs Sublime Text 2 Package
=============================

Overview
--------
This snippet provides a nearly complete set of snippets for the nodejs 0.6.x namespace.

By setting your file type to JavaScript, and selecting `Tools -> Build Systems -> Nodejs` when you
type certain namespaces and then Ctrl + Space, you will get autocomplete suggestions in the context menu.

For example, type `fs` then Ctrl + Space, you get this:

![A picture of the file system context menu](http://i.imgur.com/ZCFcC.png)

Install
-------

You may install `Nodejs` via the Sublime Text 2 package manager, or using git
with the below commands:

*MacOSX*

    `git clone git://github.com/tanepiper/SublimeText-Nodejs.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Nodejs`

*Windows*

    `git clone git://github.com/tanepiper/SublimeText-Nodejs.git %APPDATA%\Sublime Text 2\Packages\Nodadejs`

Build Systems
-------------

If you have a JavaScript file open, by selecting selecting `Tools -> Build Systems -> Nodejs` and
then hitting Ctrl + B, you will activate the node build system on your file and node will try to run it.
You may need to add a `path` variable to the settings object for this if your node executable is not found

Node Commands
-------------

You can access node commands in two ways.

* Via the menu in `Tools -> Node`
* By accessing the Command Palette and typing `node`

The current commands available are:

* Run current script in node
* Run current script in node with arguments
* Run current directory with node
* Run current script in node with arguments
* NPM command

Boilerplate Code
----------------

There are now some boilerplate snippets included with this package, they include
functionality such as a http server, reading the contents of a directory, etc.

To access these snippets type `node` in your editor followed by Ctrl + Space

If you have any boilerplate code you would like to see in here, get in touch.

Possible Improvements
---------------------
* [FIXED] Fix files it has a problem reading like assert and event
* See if a better Sublime file format can be generated for language stuff
* [FIXED] Add boilerplate snippets (http(s) servers, crypto functions, etc)

Documentation Building
----------------------

The script that generates the Sublime Snippets is included with this plugin.
To run it, on your command line type the following:

    cd /path/to/Sublime Text 2/Packges/Nodejs
    ./doc_builder.js -f -g -o ./Snippets

This will generate all the nodejs namespace and library snippet files.  Type `./doc_builder.js --help` for more options

Author & Contributors
----------------------
[Tane Piper](http://twitter.com/tanepiper) - if you find this plugin useful then please ping me if you would like to
donate to my Sublime Text 2 licence fund

