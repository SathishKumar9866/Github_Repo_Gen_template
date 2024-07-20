import os
import requests

from CRUD.util import run_command, load_config
from CRUD.git import git_add_commit_push
from termcolor import colored

CONFIG_FILE = r'config.yaml'
config = load_config(config_file=CONFIG_FILE)

def check_github_repo_exists(user, repo_name):
    try:
        url = f"https://api.github.com/repos/{user}/{repo_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print(colored(f"Unexpected response from GitHub API: {response.status_code}", 'yellow'))
            return False
    except Exception as e:
        print(colored(f"Error checking GitHub repository existence: {e}", 'red'))
        
def delete_local_repo(directory):
    try:
        if os.path.exists(directory):
            run_command(f'rm -rf {directory}')
            print(colored(f"Local repository '{directory}' deleted successfully.", 'green'))
        else:
            print(colored(f"Directory '{directory}' does not exist.", 'yellow'))
    except Exception as e:
        print(colored(f"Error deleting local repository: {e}", 'red'))

def delete_remote_repo(repo_owner, repo_name, github_token):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print(colored(f"Repository '{repo_name}' deleted successfully from GitHub.", 'green'))
        else:
            print(colored(f"Failed to delete repository '{repo_name}' from GitHub. Status code: {response.status_code}", 'red'))
            print(colored(f"Response: {response.text}", 'red'))
    except requests.RequestException as e:
        print(colored(f"HTTP Request error: {e}", 'red'))
    except Exception as e:
        print(colored(f"Error deleting repository from GitHub: {e}", 'red'))

def remove_git_repo(directory_to_remove, repo_name, remove_remote=False):
    try:
        delete_local_repo(directory_to_remove)
        if remove_remote:
            github_token = config.get('github_token')
            repo_owner = config.get('github_user')
            if github_token and repo_owner:
                delete_remote_repo(repo_owner, repo_name, github_token)
            else:
                print(colored("GitHub token or username not found in config file.", 'red'))
    except Exception as e:
        print(colored(f"Error removing Git repository: {e}", 'red'))

def delete_github_repo(user, repo_name):
    try:
        if not check_github_repo_exists(user, repo_name):
            print(colored(f"GitHub repository '{user}/{repo_name}' does not exist.", 'yellow'))
            return
        confirm_delete = input(colored(f"Are you sure you want to delete '{user}/{repo_name}'? (y/n): ", 'yellow')).strip().lower()
        if confirm_delete != 'y':
            print(colored("Deletion cancelled.", 'yellow'))
            return

        github_token = config.get('github_token')
        url = f"https://api.github.com/repos/{user}/{repo_name}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print(colored(f"Repository '{repo_name}' deleted successfully from GitHub.", 'green'))
        else:
            print(colored(f"Failed to delete repository '{repo_name}' from GitHub. Status code: {response.status_code}", 'red'))
            print(colored(f"Response: {response.text}", 'red'))
    except Exception as e:
        print(colored(f"Error deleting repository from GitHub: {e}", 'red'))