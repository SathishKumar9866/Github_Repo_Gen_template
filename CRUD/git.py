import os
import subprocess
from CRUD.util import run_command
from termcolor import colored

def gh_authenticate():
    try:
        run_command('gh auth status')
    except SystemExit:
        print(colored("GitHub CLI is not authenticated. Please run 'gh auth login' first.", 'red'))
        exit(1)

def clone_repo(user, repo_name):
    repo_dir = repo_name
    if os.path.exists(repo_dir):
        print(colored(f"Directory '{repo_dir}' already exists. Removing it.", 'yellow'))
        run_command(f'rm -rf {repo_dir}')  # Use 'rmdir /s /q' for Windows
    try:
        run_command(f'git clone https://github.com/{user}/{repo_name}.git')
    except subprocess.CalledProcessError as e:
        print(colored(f"Error cloning repository: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))

def initialize_git_repo(repo_name):
    try:
        os.chdir(repo_name)
        run_command('git init')
        run_command('git config --global init.defaultBranch main')
    except FileNotFoundError as e:
        print(colored(f"Error: {e}. Directory '{repo_name}' not found.", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))

def git_add_commit_push(commit_message="Initial commit with README, requirements, Dockerfile, and .gitignore"):
    try:
        run_command('git add .')
        run_command(f'git commit -m "{commit_message}"')
        run_command('git push -u origin main')
    except subprocess.CalledProcessError as e:
        print(colored(f"Error committing and pushing changes: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))

