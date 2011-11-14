var doc_builder = require('./doc_builder').doc_builder
var path = require('path');

var p = path.resolve(__dirname + '\\..\\Snippets');

doc_builder({
  global: true,
  full: true,
  output: p
}, function() {
  console.log('Done');
});

