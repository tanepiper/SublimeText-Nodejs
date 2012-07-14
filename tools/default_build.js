var doc_builder = require('./doc_builder').doc_builder
var path = require('path');

var p = path.resolve(__dirname + '/../Nodejs.sublime-completions');

doc_builder({
  global: true,
  full: true,
  output: p,
  type: 'completions',
  expert: false
}, function() {
  console.log('Done');
});


