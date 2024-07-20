import subprocess
import yaml

import os
import subprocess
import requests
import yaml
from CRUD.util import run_command, load_config
from CRUD.git import git_add_commit_push
from termcolor import colored

from CRUD.delete import remove_git_repo

CONFIG_FILE = r'config.yaml'
config = load_config(config_file=CONFIG_FILE)

def create_github_repo(user, repo_name, description, private, delete_if_exists=False):
    try:
        privacy_flag = '--private' if private else '--public'
        if delete_if_exists:
            run_command(f'gh repo delete {user}/{repo_name} --confirm')
        run_command(f'gh repo create {user}/{repo_name} --description "{description}" {privacy_flag}')
    except subprocess.CalledProcessError as e:
        print(colored(f"Error creating GitHub repository: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))


        return False

def create_repo_and_commit(directory, delete_if_exists=False):
    try:
        if os.path.exists(directory):
            print(colored(f"Directory '{directory}' already exists. Skipping repository creation.", 'yellow'))
            if delete_if_exists:
                print(colored(f"Deleting existing directory '{directory}'...", 'yellow'))
                run_command(f'rm -rf {directory}')
                directory = input("Enter the local directory of the repository to delete: ").strip()
                repo_name = os.path.basename(os.path.normpath(directory))
                remove_remote = input("Delete the remote GitHub repository as well? (y/n): ").strip().lower() == 'y'
                remove_git_repo(directory, repo_name, remove_remote=remove_remote)

        os.makedirs(directory, exist_ok=True)
        os.chdir(directory)
        run_command('git init')

        create_github_repo(config['github_user'], os.path.basename(directory), config['description'], config['private'], delete_if_exists)

        create_readme(os.path.basename(directory))
        create_requirements(config['dependencies'])
        create_dockerfile(os.path.basename(directory), config['python_version'])
        create_gitignore()

        run_command('git add README.md')
        run_command('git commit -m "first commit"')
        # run_command('git branch -M main')
        run_command(f'git remote add origin https://github.com/{config["github_user"]}/{os.path.basename(directory)}.git')
        run_command('git push -u origin main')

        run_command('git add .')
        run_command('git commit -m "Initial commit with README, requirements, Dockerfile, and .gitignore"')
        run_command('git push -u origin main')
    except FileNotFoundError as e:
        print(colored(f"Error creating repository: {e}. Directory '{directory}' not found.", 'red'))
    except Exception as e:
        print(colored(f"Error creating repository and committing: {e}", 'red'))

def create_readme(repo_name):
    try:
        readme_content = f"""
# {repo_name}

This repository was created automatically using a script generated using ChatGPT.

## Project Description

{repo_name} is a sample repository created to demonstrate automation in setting up a GitHub repository, including initializing git, creating essential files, and pushing them to GitHub.

## How to Use

- Clone the repository
- Follow the instructions in the Dockerfile to build and run the application
"""
        with open('README.md', 'w') as file:
            file.write(readme_content.strip())
    except Exception as e:
        print(colored(f"Error creating README.md file: {e}", 'red'))

def create_requirements(dependencies):
    try:
        with open('requirements.txt', 'w') as file:
            for dependency in dependencies:
                file.write(f"{dependency}\n")
    except Exception as e:
        print(colored(f"Error creating requirements.txt file: {e}", 'red'))

def create_dockerfile(repo_name, python_version):
    try:
        dockerfile_content = f"""
# Use the official Python image from the Docker Hub
FROM python:{python_version}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME {repo_name}

# Run app.py when the container launches
CMD ["python", "app.py"]
"""
        with open('Dockerfile', 'w') as file:
            file.write(dockerfile_content.strip())
    except Exception as e:
        print(colored(f"Error creating Dockerfile: {e}", 'red'))

def create_gitignore():
    try:
        gitignore_content = """
# Ignore config.yaml file
config.yaml
"""
        with open('.gitignore', 'w') as file:
            file.write(gitignore_content.strip())
    except Exception as e:
        print(colored(f"Error creating .gitignore file: {e}", 'red'))
