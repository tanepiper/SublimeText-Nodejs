Nodejs Sublime Text 2 Package
=============================

Overview
--------
This snippet provides a nearly complete set of snippets for the nodejs 0.6.x namespace.

By setting your file type to JavaScript, and selecting `Tools -> Build Systems -> Nodejs` when you
type certain namespaces and then Ctrl + Space, you will get autocomplete suggestions in the context menu.

For example, type `fs` then Ctrl + Space, you get this:

![A picture of the file system context menu](http://i.imgur.com/QLVPt.jpg)

Install
-------

MacOSX

    `git clone git://github.com/tanepiper/SublimeText-Nodejs.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Nodejs`

Windows

    `git clone git://github.com/tanepiper/SublimeText-Nodejs.git %APPDATA%\Sublime Text 2\Packages\Nodadejs`

Build Systems
-------------

If you have a JavaScript file open, by selecting selecting `Tools -> Build Systems -> Nodejs` and
then hitting Ctrl + B, you will activate the node build system on your file and node will try to run it.

Currently it does not accept arguments, and you may need to close Sublime Text to end your process if it's
long running - these are currently being looked in to.

Possible Improvements
---------------------
* Fix files it has a problem reading like assert and event [Fixed]
* See if a better Sublime file format can be generated for language stuff
* Add boilerplate snippets (http(s) servers, crypto functions, etc)

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

