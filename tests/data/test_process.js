var process = require("process");

// the cwd()
console.info("The current working dir is -", process.cwd(), "\n");

console.info("The args count is -", process.argv.length);

// the argv
console.info("The args passed to the script is -");
process.argv.forEach(function (val, index, arr) {
    console.info(index, val);  
});

// the envs 
console.info("\nThe environment varibales is -");
Object.keys(process.env).forEach(function (val, index, arr) {
    console.info(val, "=>", process.env[val]);
});