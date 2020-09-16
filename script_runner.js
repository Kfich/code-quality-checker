var shell = require('shelljs');
var fs = require('fs');


// directory is the data read from git_url.txt
fs.readFile("./git_url.txt", 'utf8', function(err, directory) {
	parent_directory = "data-" + directory;

	// Check Number of comments, number of lines of code, etc.
	console.log("Get number of comments");
	if (shell.exec('cloc --json ./' + directory + '> ' + parent_directory + '/file_data.json').code !== 0) {
	}


	// Check Dependency, for updates
	console.log("Checking for dependency updates");
	if (shell.exec('ncu -j --packageFile ' + directory + '/package.json > ' + parent_directory + '/ncu.json').code !== 0) {
	}



	// Check Dependency, for unused modules
	console.log("Checking for unused dependencies");
	if (shell.exec('depcheck ./' + directory + ' --json > ' + parent_directory + '/depcheck.json').code !== 0) {
	}


	// Check santax, create html
	console.log("Checking Santax, Creating HTML file");
	if (shell.exec('eslint -c configuration.eslintrc -f html ' + directory + '/*.js ' + directory + '/*/*.js > ' + parent_directory + '/results.html').code !== 0) {
	}


	// Check santax, create json
	console.log("Checking Santax, Creating JSON file");
	if (shell.exec('eslint -c configuration.eslintrc -f json ' + directory + '/*.js ' + directory + '/*/*.js > ' + parent_directory + '/results.json').code !== 0) {
		shell.exit(1);
	}

});

