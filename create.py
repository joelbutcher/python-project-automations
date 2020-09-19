"""
Name: Python Create Project Automation.
Author: Joel Butcher
Date: 18/09/2020
This Python script is designed to run as a cli tool, accepting the project name as the only argment.
The script will, navigate to your desired projects path, create a new project folder and a README markdown document.
It will then create a new repo using your Github access token and commit the project + README.md to the remote origin.
Note: This file requires you to install the PiGithub Python dependency.
Optional:
If desired, this Python script can be embedded into a bash command for additional automation. To do so, simply specify
the bash argument '$1' as the first argument to the script.
e.g. `python create.py $1`
"""

import sys
import os
import errno
from github import Github

projectName = sys.argv[1]

path = "YOUR_PROJECTS_PATH"
githubToken = "YOUR_GITHUB_ACCESS_TOKEN"
githubUsername = 'YOUR_GITHUB_USERNAME'

def getGithub():
	return Github(githubToken)

def findOrCreateRepo(githubUser):
	repo = findRepo(githubUser)

	# If the repo already exists, clone it,
	# otherwise, create a new repo with an initial commit
	if repo != False:
		cloneRepo(repo)

		# If the clone repo is empty, create an initial commit
		if [f for f in os.listdir(path + projectName) if not f.startswith('.')] == []:
			newInitialCommit(repo)
	else:
		print('Could not find existing repo, creating a new one...')
		repo = createRepo(githubUser)

	return repo

def findRepo(githubUser):
	repo = False
	# First, fetch all the repo's for the users
	# to see if one already exists on the account.
	print('Searching for existing repo %s' %(projectName,))
	for githubRepo in githubUser.get_repos():
		if (githubRepo.name == projectName):
			repo = githubRepo
	return repo

def createRepo(githubUser):
	githubUser.create_repo(projectName)
	print('Created repo %s/%s' %(githubUsername, projectName,))
	repo = githubUser.get_repo(projectName)
	newInitialCommit(repo)
	return repo

def cloneRepo(repo):
	# Change directory to the specified path
	os.chdir(path)
	# Clone repo in current working directory - repo.clone_url
	# git@github.com:joelbutcher/laravel-make-commands.git
	os.system('git clone git@github.com:%s/%s.git' %(githubUsername, projectName,))
	print('Successfully cloned repo %s/%s' %(githubUsername, projectName,))

def newInitialCommit(repo):
	# Create new README.md
	f = open('README.md', 'w')
	f.write('# %s' % (projectName))
	f.close()
	# Commit and push README.md
	fileContents = open('README.md', 'r').read()
	repo.create_file('README.md', 'Initial commit', fileContents)
	print('Successfully pushed initial commit')

def create():
	g = getGithub()
	# First, let's check Github for an existing project that matches the entered name
	# If one doesn't exist, we'll create it and push an initial commit
	# If one does exist, we'll clone it, and only push an itial commit
	# if the cloned project is empty.
	repo = findOrCreateRepo(g.get_user())

	# If the repo could not be found or created, exit with error message
	if repo == False:
		exit('Could not find or create repository %s/%s' %(githubUsername, projectName))

	# Change directory to the new project folder
	os.chdir(path + projectName)

if __name__ == "__main__":
	if os.path.exists(path + projectName):
		os.chdir(path + projectName)
		exit("Project already exists, please use a different name.")
	# Project doesnt exist, let's create a new one
	create()
