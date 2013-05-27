var commander = require('commander');
var minify = require("uglify-js").minify;
var path = require('path');
var fs = require('fs');


var uglify_data = function(data, cb) {
  var orig_code = data.join("\n");
  var final_code = minify(orig_code, { fromString: true }).code;

  cb(null, final_code);
}

var open_file = function(filename, cb) {
  fs.readFile(filename, cb)
}


var startUglify = function (options) {
  if (!options.input) {
    throw new Error('You need to pass at least 1 file to this script via -i');
  }
  var i = 0, j = options.input.length;
  var data_collection = [];
  for(;i<j;i++) {
    var filepath = path.resolve(options.input[i]);
    open_file(filepath, function(err, data) {
      if (err) throw err;
      data_collection.push(data);

      if (data_collection.length === j) {
        uglify_data(data_collection, function(err, data) {
          if (err) throw err;
          if (options.output) {
            var outpath = path.resolve(options.output);
            fs.writeFile(outpath, function(err) {
              if (err) throw err;
            })
          } else {
            console.log(data);
          }
          
        });
      }
    });
  }
}


function list(val) {
  return val.split(',');
}

commander
  .version('1.0.0')
  .option('-i --input <items>', 'A filename or filepath to uglify', list)
  .option('-o --output [value]', 'The location of the output file')
  .parse(process.argv);


  startUglify(commander);
