/**
 * This file allows me to build the snippet files by reading the nodejs lib
 * files.
 * It uses autodoc which itself has some dependencies
 * 
 */

var fs = require('fs');
var exec = require('child_process').exec;
var path = require('path');

var nodelib = path.resolve('C:\\Users\\tanepiper\\Desktop\\nodelib');
console.log('Node Lib ' + nodelib);
var autodoc = path.resolve('C:\\Users\\tanepiper\\source\\node-autodoc\\autodoc.co');
console.log('Autodoc Path ' + autodoc);

var snippet_path = path.resolve('C:\\Users\\tanepiper\\AppData\\Roaming\\Sublime Text 2\\Packages\\Nodejs\\Snippets');


/**
 * Process the buffer from the stdout and join together on end
 * @param  {FileHandler} spw The file handler
 * @param  {FUnction} cb  Callback
 * @return none
 */
var processBuffer = function(spw, cb) {
  var buf = '';
  spw.stdout.on('data', function(data) {
    buf += data;
  });
  spw.stdout.on('end', function() {
    cb(buf);
  });
};

/**
 * Execture the file and read the data, pass to callback when done
 * @param  {[type]} fileobj [description]
 * @param  {[type]} cb      [description]
 * @return {[type]}
 */
var execFile = function(fileobj, cb) {
  var s = exec('coco ' + autodoc + ' ' + fileobj.nodelib);

  var data = '';
  s.stdout.on('data', function(d) {
    data += d;
  });

  s.stdout.on('end', function(){
    cb(data);
  });
}

var createSnippet = function(file, key, args) {
  var args_joined_array = [];

  if (args && args.length > 0) {
    var i = 0, j = args.length;
    for(;i<j;i++) {
      args_joined_array.push(args[i].name);
    }
  }
  var args_joined = args_joined_array.join(', ');
  var output = [];
  output.push('<snippet>');
    output.push('   <content>' + file + '.' + key + '(' + args_joined + ');</content>');
    output.push('   <tabTrigger>'+ file + '.' + key + '</tabTrigger>');
    output.push('   <scope>source.js</scope>');
    output.push('   <description>' + file + '.' + key + '</description>');
  output.push('</snippet>');
  //console.log(output.join("\n"));
  saveFile(file, key, output.join("\n"));
}

var saveFile = function(file, key, output) {
  fs.writeFile(path.resolve(snippet_path, 'node-' + file + '-' + key + '.sublime-snippet'), output);
}
 
var readFile = function(filename) {
  var fileobj = {
    filename: filename,
    basename: path.basename(filename, '.js'),
    nodelib: path.resolve(nodelib, filename)
  }
  execFile(fileobj, function(data) {
    var obj;
    try {
      obj = JSON.parse(data);
    } catch(exp) {
      //console.log(fileobj.basename, exp);
    }
    console.log(fileobj.basename, obj);

    var key;
    if (obj && obj.properties) {
      for(key in obj.properties) {
        createSnippet(fileobj.basename, key, obj.properties[key].args);
      }
    }
  });
}

var readdir = function(err, files) {
  if (err) throw err;

  var i = 0, j = files.length;
  for(;i<j;i++) {
    readFile(files[i]);
  }
}

fs.readdir(nodelib, readdir);
