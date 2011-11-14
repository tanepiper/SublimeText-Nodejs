#!/usr/bin/env node

var fs = require('fs');
var path = require('path');
var commander = require('commander');

/**
 * This function is called to render the snippet from the passed object
 * and to save it to it's sublime-snippet file
 * @param  {Commander} commander The command line interface
 * @param  {Array} snippets An array of snippet objects
 * @return {void}
 */
var createSnippets = function(commander, snippets) {

  // Loop over each snippet and save to file
  var i = 0, j = snippets.length;
  for(;i<j;i++) {
    var item = snippets[i];

    // TODO: Template this so supports other output formats
    var output = [];
    output.push('<snippet>');
      output.push('   <content>' + item.function_string + '</content>');
      output.push('   <tabTrigger>'+ [item.type, item.name].join('.') + '</tabTrigger>');
      output.push('   <scope>source.js</scope>');
      output.push('   <description>' + item.args + '</description>');
    output.push('</snippet>');

    // Call save
    saveFile(commander, item, output.join("\n"));
  }

}

/**
 * If an output path is specified then the files will be output to that directory
 * as individual snippet files.  If not file is specified then it is output to
 * console which can be piped into a file
 * @param  {[type]} commander [description]
 * @param  {[type]} item      [description]
 * @param  {[type]} output    [description]
 * @return {[type]}
 */
var saveFile = function(commander, item, output) {
  if (commander.output) {
    var dest_path = path.resolve(commander.output, item.type);

    fs.mkdir(dest_path, 0755, function() {
      var file_path = path.resolve(dest_path, 'node-' + item.type + '-' + item.name + '.sublime-snippet');
      fs.writeFile(file_path, output);
    });
  } else {
    console.log(output);
  }
}

/**
 * Taken and slightly modified to support args, from http://hiveminds.org/phpBB/viewtopic.php?t=2885
 * @param {Function} fn function to be reflected
 */
var FunctionReflect = function(fn) {
   this.fn = fn;

   var s = fn.toString();
   var iOpenParams = s.indexOf('(');
   var closeParams = s.indexOf(')');
   this.name = s.substring(s.indexOf('function') + 8, iOpenParams);
   this.name = this.name.trim();

   this.params = s.slice(iOpenParams, closeParams + 1);

   this.className = null;
   this.methodName = null;
   var iUnderscore = this.name.indexOf('_');

   if(iUnderscore >= 0) {
      this.className = this.name.substr(0, iUnderscore);
      this.methodName = this.name.substr(iUnderscore + 1);
   }

   this.body = s.substring(s.indexOf('{') + 1, s.indexOf('}') - 1);
   return this;
}

/**
 * Function to extract global functions not included in source files or requires
 * @param  {Array} output The output array to put the data in to
 * @return {Array} The output array
 */
var createGlobals = function(output) {
  var gKey;
  for (gKey in global) {
    if (typeof global[gKey] === 'function') {
      var snippet = {
        type: 'global',
        name: gKey,
        reflection: FunctionReflect(global[gKey])
      }
      snippet['args'] = snippet.reflection.params.trim();
      snippet['function_string'] = '' + [snippet.type, snippet.name].join('.') + snippet.reflection.params.trim() + ';'
      output.push(snippet);
    }
  }

  var pKey
  for (pKey in process) {
    if (typeof process[pKey] === 'function') {
      var snippet = {
        type: 'process',
        name: pKey,
        reflection: FunctionReflect(process[pKey])
      }
      snippet['args'] = snippet.reflection.params.trim();
      snippet['function_string'] = '' + [snippet.type, snippet.name].join('.') + snippet.reflection.params.trim() + ';'
      output.push(snippet);
    }
  }

  var rKey
  for (rKey in require) {
    if (typeof require[rKey] === 'function') {
      var snippet = {
        type: 'require',
        name: rKey,
        reflection: FunctionReflect(require[rKey])
      }
      snippet['args'] = snippet.reflection.params.trim();
      snippet['function_string'] = '' + [snippet.type, snippet.name].join('.') + snippet.reflection.params.trim() + ';'
      output.push(snippet);
    }
  }

  return output;
}

/**
 * Iterate over the node libs and generate snippets for each one
 * @param  {[type]} commander [description]
 * @param  {[type]} output    [description]
 * @return {[type]}
 */
var createNodeLibs = function(commander, output) {
  var files = [
    '_debugger', '_linklist', 'assert', 'buffer', 'buffer_ieee754',
    'child_process', 'cluster', 'console', 'constants', 'crypto',
    'dgram', 'dns', 'events', 'freelist', 'fs', 'http', 'https',
    'module', 'net','os', 'path', 'punycode', 'querystring',
    'readline', 'repl', 'stream', 'string_decoder', 'sys',
    'timers', 'tls', 'tty',  'url','util', 'vm', 'zlib'
  ];

  createNamespaces(files, output);
}


/**
 * Experimental command to create docs from specific files from a directory
 * @param  {[type]} commander [description]
 * @param  {[type]} output    [description]
 * @return {[type]}
 */
var loadDirectory = function(commander, output) {
  var source_path = path.resolve(commander.input);

  fs.readdir(source_path, function(error, items) {
    if (error) throw error;
    var i = 0, j = items.length;
    for(;i<j;i++) {
      var item = items[i];
      if (item.indexOf('.js') > -1) {
        var p = path.basename(item, '.js');
        var r = require(path.resolve(source_path, p));
        var rkey;
        for(rkey in r) {
          if (r.hasOwnProperty(rkey)) {
            if (typeof r[rkey] === 'function') {
              var doc_output = {}
              doc_output.type = p;
              doc_output.key = rkey;
              doc_output.reflection = FunctionReflect(r[rkey]);
              doc_output.args = doc_output.reflection.params.trim();
              doc_output.f_string = '' + doc_output.key + doc_output.reflection.params.trim();
              doc_output.name = '' + doc_output.key;
              output.push(doc_output);
            }
          }
        }
      }
    }
  });
}

/**
 * A function to take an array of namespaces and output them to the docs
 * @param  {[type]} commander [description]
 * @param  {[type]} output    [description]
 * @return {[type]}
 */
var createNamespaces = function(ns, output) {
  var i = 0, j = ns.length;
  for(;i<j;i++) {
    var item = require(ns[i]);
    var rKey
    for (rKey in item) {
      if (typeof item[rKey] === 'function') {
        var snippet = {
          type: ns[i],
          name: rKey,
          reflection: FunctionReflect(item[rKey])
        }
        snippet['args'] = snippet.reflection.params.trim();
        snippet['function_string'] = '' + [snippet.type, snippet.name].join('.') + snippet.reflection.params.trim() + ';'
        output.push(snippet);
      }
    }
  }
}

/**
 * Small helper function for the command line to split out namespace options
 * @param  {String} val The values to be split
 * @return {Array} An array of values to iterate over
 */
function list(val) {
  return val.split(',');
}

/**
 * Main commander program for our input.  Checks incoming args and based on this
 * parses the required files
 */
commander
  .version('1.0.1')
  .option('-i --input <value>', 'The input path where the source code is located')
  .option('-o --output <value>', 'The location of the output file')
  .option('-n --ns [namespaces]', 'The namespaces you wish to include as a comma separated list', list)
  .option('-g --global', 'Add the global namespaces (global, process, console)')
  .option('-f --full', 'Include the whole nodejs standard library')
  .parse(process.argv);

var output = [];

if (commander.global) {
  createGlobals(output);
}

if (commander.ns) {
  createNamespaces(commander, output);
}

if (commander.full) {
  createNodeLibs(commander, output);
}

if(commander.input && commander.output) {
  loadDirectory(commander, output);
}

createSnippets(commander, output);


exports.run = function(options) {
  var output = [];
  if (options.global) {
    createGlobals(output);
  }
  if (options.ns) {
    createNamespaces(commander, output);
  }
  if (options.full) {
    createNodeLibs(commander, output);
  }
  if(options.input && commander.output) {
    loadDirectory(commander, output);
  }
  createSnippets(commander, output);
}