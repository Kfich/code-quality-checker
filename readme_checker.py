from stemming.porter2 import stem
from git import Repo
import nltk
import re
from Naked.toolshed.shell import execute_js
import json
import os
import ntpath
import os.path

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from flask import Flask, jsonify, render_template, request, url_for, send_from_directory, make_response


app = Flask(__name__)


repo_url = ''
@app.route('/git_url', methods=['POST', "GET"])
def get_repo():
    # Read data
    user_input = request.get_json(silent=True)
    repo_url = user_input["git_url"]


    val = URLValidator()
    try:
    	val(repo_url)
    	main(repo_url)
    	return ("Successful")
    except ValidationError as e:
    	return ("MalFormedURL")



def main(repo_url):
	############################ Clone Repo and Create Folder ####################################
	print('Cloning Repo')
	folder_name = repo_url.split("https://github.com/")[1].replace('/', '-')
	data_folder_name = 'data-' + folder_name



	if not os.path.exists(folder_name):
		Repo.clone_from(repo_url, folder_name)
	else:
		print("Cannot Clone because folder already exists")

	if not os.path.exists(data_folder_name):
		os.makedirs(data_folder_name)
	else:
		print("Cannot Create Folder Because Folder Already Exist")



	# Create folder to store repo url
	with open('git_url.txt', 'w') as url_file:
		url_file.write(folder_name)


	if not os.path.exists(folder_name + "/package.json"):
		print("File doesn't exist")
		output_json = {}
		output_json['Error_Boolean'] = True

		with open('static/output.json', 'w') as outfile:
		    json.dump(output_json, outfile)
		    print("Creating Output File")

		with open(data_folder_name + '/output.json', 'w') as outfile:
		    json.dump(output_json, outfile)

	else:


		############################## Read File ####################################
		print('Reading README')
		with open(folder_name + "/README.md") as file:
		    readme_words = file.read().split()

		with open(folder_name + "/README.md") as file:
		    lines = file.readlines()



		############################### Get Key Words #################################
		key_words_array = []


		# List of key words
		repo_keywords = "Installation Running Install Usage Example Documentation Getting Started Requirements Contribution Test License Quick Start API"
		key_words = nltk.word_tokenize(repo_keywords)


		for word in key_words:
		    key_words_array.append(word)



		############################### Get data ######################################
		print('Getting Data')
		number_of_lines = len(lines)

		image_count = 0
		number_of_headings = 0
		number_of_keywords = 0

		for word in readme_words:

		    if (word == '##' or word == '#' or word == '###' or word == '####' or word == '#####' ):
		        number_of_headings += 1
		    if (word in key_words_array):
		        number_of_keywords += 1


		    # Look for images
		    images = re.findall('.png', word)
		    if (images != []):
		        image_count += 1




		################################ Compute Final Score #########################
		print('Computing Score')
		final_object = {}
		readme_object = {}


		final_score = 0

		if (number_of_headings <= 2):
		    final_score += 1
		    readme_object["Organization"] = "Documentation is not very organized"

		elif (number_of_headings <= 6):
		    final_score += 2
		    readme_object["Organization"] = "Documentation is organized"

		elif (number_of_headings > 6):
		    final_score += 4
		    readme_object["Organization"] = "Documentation is very organized"



		if (number_of_keywords <= 2):
		    final_score += 1
		    readme_object["Clarity"] = "Documentation is not very clear"

		elif (number_of_keywords <= 6):
		    final_score += 2
		    readme_object["Clarity"] = "Documentation is clear"

		elif (number_of_keywords >= 9):
		    final_score += 4
		    readme_object["Clarity"] = "Documentation is very clear"



		if (number_of_lines <= 10):
		    final_score += 1
		    readme_object["number_of_lines"] = "Short Documentation"

		elif (number_of_lines <= 25):
		    final_score += 2
		    readme_object["number_of_lines"] = "Good Documentation"

		elif (number_of_lines >= 40):
		    final_score += 4
		    readme_object["number_of_lines"] = "Very Detailed Documentation"


		if (image_count == 1):
			final_score += 2
		if (image_count > 1):
			final_score += 4

		if (image_count == 0):
		    readme_object["Images"] = "Documentation has no images"
		else:
		    readme_object["Images"] = "Documentation contains images"



		readme_object["Number of sections"] = str(number_of_headings)
		readme_object["Documentation Length"] = str(len(lines))
		readme_object["Number_of_Key_Words"] = str(number_of_keywords)
		readme_object["Documentation Score"] = str(final_score)


		final_object['readme'] = readme_object



		with open(data_folder_name + '/readme_score.json', 'w') as outfile:
		    json.dump(final_object, outfile)



		################################### Run node files ###########################
		print('Running Node Script')
		success = execute_js('script_runner.js')













			############################## Read Files ####################################
		print("Final Grader Running")
		with open('git_url.txt', 'r') as url_file:
		        data_folder_name = "data-" + url_file.read()


		with open(data_folder_name + '/results.json') as data_file:
		    results_data = json.load(data_file)


		with open(data_folder_name + '/file_data.json') as data_file:
		    file_data = json.load(data_file)


		with open(data_folder_name + '/ncu.json') as data_file:
		    ncu_data = json.load(data_file)


		with open(data_folder_name + '/depcheck.json') as data_file:
		    depcheck_data = json.load(data_file)


		with open(data_folder_name + '/readme_score.json') as data_file:
		    readme_data = json.load(data_file)


		with open(folder_name + '/package.json') as file:
			package_data = json.load(file)



		################################### File Data ###############################
		# Find the total number of 'serious' errors in each file
		total_errors = 0
		file_error_array = []
		for i in range(0, len(results_data)):
		    file_name = ntpath.basename(results_data[i]['filePath'])
		    file_errors = {}
		    file_errors[file_name] = {}
		    file_errors[file_name]["Errors"] = results_data[i]["errorCount"] - results_data[i]["fixableErrorCount"]
		    file_errors[file_name]["Warnings"] = results_data[i]["warningCount"] - results_data[i]["fixableWarningCount"]
		    file_error_array.append(file_errors)
		    total_errors += results_data[i]["errorCount"] - results_data[i]["fixableErrorCount"]



		################################### Module Data  ###############################
		all_modules = []

		if ("devDependencies" in package_data):
			for mod in package_data["devDependencies"]:
				all_modules.append(mod)

		if ("optionalDependencies" in package_data):
			for mod in package_data["optionalDependencies"]:
				all_modules.append(mod)

		if ("dependencies" in package_data):
			for mod in package_data["dependencies"]:
				all_modules.append(mod)

		if ('jspm' in package_data):
			if ("dependencies" in package_data["jspm"]):
				for mod in package_data["jspm"]["dependencies"]:
					all_modules.append(mod)

		if ('jspm' in package_data):
			if ("devDependencies" in package_data["jspm"]):
				for mod in package_data['jspm']["devDependencies"]:
					all_modules.append(mod)





		# Find which modules need to be updated
		modules_update_array = []
		if ("devDependencies" in ncu_data):
		    dev_keys = list(ncu_data["devDependencies"].keys())
		    for j in range(0, len(dev_keys)):
		        modules = {}
		        modules[dev_keys[j]] = ncu_data["devDependencies"][dev_keys[j]]
		        modules_update_array.append(modules)


		if ("optionalDependencies" in ncu_data):
		    opt_keys = list(ncu_data["optionalDependencies"].keys())
		    for k in range(0, len(opt_keys)):
		        modules = {}
		        modules[opt_keys[k]] = ncu_data["optionalDependencies"][opt_keys[k]]
		        modules_update_array.append(modules)

		if ("dependencies" in ncu_data):
			d_keys = list(ncu_data['dependencies'].keys())
			for l in range(0, len(d_keys)):
				modules = {}
				modules[d_keys[l]] = ncu_data['dependencies'][d_keys[l]]
				modules_update_array.append(modules)



		# Find what percentage of the code are comments
		comment_density = file_data['JavaScript']['comment'] / file_data['JavaScript']['code']
		comment_density = ("%.2f" % (comment_density * 100))



		# Remove testing modules, we aren't concerned if they are outdate
		testing_mods = ['mocha', 'jest', 'enzyme', 'chai', 'electron', 'electron-builder', 'rimraf', 'babel', 'gulp', 'bluebird']

		if ("optionalDependencies" in ncu_data and "devDependencies" in ncu_data and "dependencies"):
			non_testing_mods = list(ncu_data["devDependencies"].keys()) + list(ncu_data["optionalDependencies"].keys()) + list(ncu_data["dependencies"].keys()) 
			non_testing_mods = [x for x in non_testing_mods if x not in testing_mods]

			for test_mod in testing_mods:
				pattern = re.compile(test_mod)
				for non_test_mod in non_testing_mods:
					if(pattern.match(non_test_mod)):
						non_testing_mods.remove(non_test_mod)


		elif ("optionalDependencies" in ncu_data):
		    non_testing_mods = list(ncu_data["optionalDependencies"].keys())
		    non_testing_mods = [x for x in non_testing_mods if x not in testing_mods]
		    for test_mod in testing_mods:
		    	pattern = re.compile(test_mod)
		    	for non_test_mod in non_testing_mods:
		    		if(pattern.match(non_test_mod)):
		    			non_testing_mods.remove(non_test_mod)

		elif ("devDependencies" in ncu_data):
			non_testing_mods = list(ncu_data["devDependencies"].keys()) 
			non_testing_mods = [x for x in non_testing_mods if x not in testing_mods]
			for test_mod in testing_mods:
				pattern = re.compile(test_mod)
				for non_test_mod in non_testing_mods:
					if(pattern.match(non_test_mod)):
						non_testing_mods.remove(non_test_mod)


		elif("dependencies" in ncu_data):
			non_testing_mods = list(ncu_data["dependencies"].keys()) 
			non_testing_mods = [x for x in non_testing_mods if x not in testing_mods]
			for test_mod in testing_mods:
				pattern = re.compile(test_mod)
				for non_test_mod in non_testing_mods:
					if(pattern.match(non_test_mod)):
						non_testing_mods.remove(non_test_mod)



		################################# Calculate Repo Final Score ###################
		# Object containing all the deductions
		deductions = {}




		# Each repo gets a base score of 100
		final_score = 100


		print("Non-testing mod", len(non_testing_mods))
		print("All-mods", len(all_modules))



		# Deduct points for out of date mods
		if (len(all_modules) != 0):
			percentage_out_of_date = len(non_testing_mods) / len(all_modules)
			print("Out of date Percent", percentage_out_of_date)


			if (percentage_out_of_date >= .75):
				final_score -= 30
				deductions['Outdated Libs'] = str(30)

			elif(percentage_out_of_date >= .50):
				final_score -= 20
				deductions['Outdated Libs'] = str(20)

			elif(percentage_out_of_date >= .25):
				final_score -= 10
				deductions['Outdated Libs'] = str(10)


		error_percentage = 0
		# Deduct points for file errors
		number_of_lines_of_code = file_data['JavaScript']['code']

		if (number_of_lines_of_code != 0):
			error_percentage = (total_errors / number_of_lines_of_code) * 100


			print("Error Percentage", error_percentage)

			if (error_percentage >= 50):
				final_score -= 25
				deductions['File Errors'] = str(25)
			elif (error_percentage >= 40):
				final_score -= 20
				deductions['File Errors'] = str(20)
			elif (error_percentage >= 30):
				final_score -= 15
				deductions['File Errors'] = str(15)
			elif (error_percentage >= 20):
				final_score -= 10
				deductions['File Errors'] = str(10)
			elif (error_percentage >= 10):
				final_score -= 5
				deductions['File Errors'] = str(5)







		# minus 25 points if the readme isn't documented well enough. 6 Points for the readme if the cut off
		readme_score = readme_data['readme']['Documentation Score']
		if (int(readme_score) < 6):
		    final_score -= 25
		    deductions['Documentation Quality'] = '25'


		# minus 25 points if the code isn't well commented. 2% is the cut off
		if (float(comment_density) < 2):
		    final_score -= 25
		    deductions['Comment Percentage'] = '25'


		print(final_score)



		################################# Create json object ##############################
		output_json = {}
		output_json['file_errors'] = file_error_array
		output_json['total_errors'] = total_errors
		output_json['comment_density'] = comment_density
		output_json['mods_to_update'] = modules_update_array
		if ("devDependencies" in ncu_data ):
		    output_json['unused_mods'] = depcheck_data["devDependencies"]
		output_json['readme'] = readme_data['readme']
		output_json['final_score'] = final_score
		output_json['deductions'] = deductions
		output_json['error_percentage'] = '{0:.3f}'.format(error_percentage)
		output_json['Error Boolean'] = False





		output_json['language_data'] = {}
		all_langauages = file_data.keys()
		for langauage in all_langauages:
			if langauage != "header":
				output_json['language_data'][langauage] = file_data[langauage]


		print(deductions)


		if (final_score < 75):
		    output_json['upgrade'] = False
		else:
		    output_json['upgrade'] = True


		if not os.path.exists("static"):
		    os.makedirs("static")



		# Stored json object in json file named output.json
		with open('static/output.json', 'w') as outfile:
		    json.dump(output_json, outfile)
		    print("Creating Output File")

		with open(data_folder_name + '/output.json', 'w') as outfile:
		    json.dump(output_json, outfile)


		################################ Flask ###########################################

	@app.route('/report')
	def display_report():
	    send_from_directory(app.static_folder, "output.json")
	    return send_from_directory(app.template_folder, "clients_message.html")


if __name__ == "__main__":
    app.run()


