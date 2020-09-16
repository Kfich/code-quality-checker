# Code-Quality-Checker

## Installation
#### Node
        npm install eslint

        npm install npm-check-updates

        npm install depcheck

        npm install shelljs

        npm install -g sloc

#### Python
        pip install GitPython

        pip install stemming

        pip install Naked

        pip install nltk (first run “import nltk download nltk()” in terminal to download)


## Running (Postman app can be used for testing)
Run

	python readme_checker.py

Make a post request to

	http://127.0.0.1:5000/<git_url>

in the format {"git_url":"url"}, where "url" is replaced by the url of the repo you want to inspect

Once the program finishes running make a GET request to

	http://127.0.0.1:5000/report

to see a detailed report of the repo's quality

## Usage
Used to check the quality of a repo and its Node.js files. Two HTML files are outputted. Results.html gives a description of all the errors in each node file. The second displays the repos quality and gives details that went into that score.

## Script_Runner.js

This file runs node shell scripts.

### Get File Date
        sloc -f json ./' + directory + '> ' + parent_directory +'/file_data.json'


       
Gets the number of lines of code and comments in each file

### Santax and Format checker

        'eslint -c configuration.eslintrc -f html ' + directory + '/*.js ' + directory + '/*/*.js > ' + parent_directory + '/results.html'

This is will check all javascript files using the rules outlined in configuration.eslintrc and output all errors in an html file named results.html

    
        'eslint -c configuration.eslintrc -f json ' + directory + '/*.js ' + directory + '/*/*.js > ' + parent_directory + 			'/results.json'

This is will check all javascript files using the rules outlined in configuration.eslintrc and output all errors in a json file named results.json

#### configuration.eslintrc
Holds all the rules to be used when checking each node file.

### Dependency Checker
#### Checking for updates

        'ncu -j --packageFile ' + directory + '/package.json > ' + parent_directory + '/ncu.json'

        
Checks the package.json in the 'directory' folder to see if any outdated modules

       ncu -u

Can be used to update all the modules


#### Checking for unused modules
=======
       'depcheck ./' + directory + ' --json > ' + parent_directory + '/depcheck.json'
       
Checks the package.json in the 'directory' and all node files for unused modules    

       'depcheck ./' + directory + ' --json > ' + parent_directory + '/depcheck.json'
       
Checks the package.json in the 'directory' and all node files for unused modules    

## Work Flow

1. Readme_checker →  git_folder 

2. Readme_checker →  data_git_folder

3. Readme_checker → git_url.txt

4. Readme_checker reads from:

	git_folder/Readme
	
5. Readme_checker → data_git_folder/readme.json

6. Readme_checker runs:

	script_runner.js

7. script_runner.js → data_git_folder/file_data.json

8. script_runner.js → data_git_folder/ncu.json

9. script_runner.js → data_git_folder/depcheck.json

10. script_runner.js → data_git_folder/result.html

11. script_runner.js → data_git_folder/result.json

12. Readme_checker reads from:

	data_git_folder/file_data.json
	
	data_git_folder/ncu.json
	
	data_git_folder/depcheck.json
	
	data_git_folder/result.json
	
14. Readme_checker→ data_git_folder/output.json

15. Readme_checker→ static

16. Readme_checker→ static/output.json

17. client_message.html reads from

	static/output.json
