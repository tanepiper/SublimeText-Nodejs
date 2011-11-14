var fs = require('fs');
var path = require('path');

var nodelib = path.resolve('C:\\Users\\tanepiper\\Desktop\\nodelib');
var snippet_path = path.resolve('C:\\Users\\tanepiper\\AppData\\Roaming\\Sublime Text 2\\Packages\\Nodejs\\Snippets');

var createSnippets = function(snippets) {
  var i = 0, j = snippets.length;
  for(;i<j;i++) {
    var item = snippets[i];

    var html_output = [];
    var html_groups = [];

    var output = [];
    output.push('<snippet>');
      output.push('   <content>' + item.f_string + '</content>');
      output.push('   <tabTrigger>'+ item.name + '</tabTrigger>');
      output.push('   <scope>source.js</scope>');
      output.push('   <description>' + item.name + '</description>');
    output.push('</snippet>');
    console.log(output.join("\n"));

    /*
    html_outp   ut.push('<div class="snippet">');
      html_output.push('<strong>' + item.name + '</strong>');
      html_output.push('<pre>' + item.reflection.body + '</pre>');
    html_output.push('</div>');

    var i = {};
    i[item.name] = html_output;
    html_groups.push(i);

    var final_groups = [];
    var hgkey;
    for (hgkey in html_groups) {
      var o = [];
      o.push('<div class="function">');
        o.push('<h2>' + hgkey + '</h2>');
        o.push(html_groups[hgkey]);
      o.push('</div>');
      final_groups.push(o);
    }
    console.log(final_groups);
    */

    saveFile(item.type, item.key, output.join("\n"));
  }

}

var saveFile = function(file, key, output) {
  fs.mkdir(path.resolve(snippet_path, file), function() {
    var p = path.resolve(snippet_path, file, 'node-' + file + '-' + key + '.sublime-snippet');
    //console.log(p);
    fs.writeFile(p, output);
  })
  
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
  
var readdir = function(err, files) {
  if (err) throw err;

  var output_arr = [];

  var i = 0, j = files.length;
  for(;i<j;i++) {

    var p = path.basename(files[i], '.js')
    var r = require(p);

    var rkey;
    for(rkey in r) {
      if (r.hasOwnProperty(rkey)) {
        if (typeof r[rkey] === 'function') {
          var doc_output = {}
          doc_output.type = p;
          doc_output.key = rkey;
          doc_output.reflection = FunctionReflect(r[rkey]);
          doc_output.args = doc_output.reflection.params.trim();
          doc_output.f_string = '' + p + '.' + rkey + doc_output.args;
          doc_output.name = '' + p  + '.' + rkey;
          
          output_arr.push(doc_output);
        }
      }
    }
  }
  var pkey;
  for(pkey in process) {
    if (typeof process[pkey] === 'function') {
      var doc_output = {}
      doc_output.type = 'process';
      doc_output.key = pkey;
      doc_output.reflection = FunctionReflect(process[pkey]);
      doc_output.args = doc_output.reflection.params.trim();
      doc_output.f_string = '' + doc_output.key + doc_output.reflection.params.trim()
      doc_output.name = '' +  doc_output.key;
      
      output_arr.push(doc_output);
    }
  }
  var gkey;
  for(gkey in global) {
    if (typeof global[gkey] === 'function') {
      var doc_output = {}
      doc_output.type = 'global';
      doc_output.key = gkey;
      doc_output.reflection = FunctionReflect(global[gkey]);
      doc_output.args = doc_output.reflection.params.trim();
      doc_output.f_string = '' + doc_output.key + doc_output.reflection.params.trim()
      doc_output.name = '' + doc_output.key;
      
      output_arr.push(doc_output);
    }
  }
  createSnippets(output_arr);
}


fs.readdir(nodelib, readdir);
