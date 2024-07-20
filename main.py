import subprocess
import yaml

import os
import subprocess
import requests
import yaml
from CRUD.util import run_command, load_config, prompt_additional_commits
from CRUD.git import git_add_commit_push
from termcolor import colored

from CRUD.create import create_repo_and_commit
from CRUD.delete import check_github_repo_exists, remove_git_repo

CONFIG_FILE = 'config.yaml'

def main():
    config = load_config(CONFIG_FILE)
    
    while True:
        print("\nGitHub Repository Management Tool")
        print("1. Create a new GitHub repository and commit initial files.")
        print("2. Delete a local and/or remote GitHub repository.")
        print("3. Check if a GitHub repository exists.")
        print("4. Add additional commits to the repository.")
        print("5. Exit")

        choice = input("Please choose an option (1-5): ").strip()

        if choice == '1':
            directory = input("Enter the local directory to create the repository in: ").strip()
            delete_if_exists = input("Delete the directory if it already exists? (y/n): ").strip().lower() == 'y'
            create_repo_and_commit(directory, delete_if_exists=delete_if_exists)
        elif choice == '2':
            directory = input("Enter the local directory of the repository to delete: ").strip()
            repo_name = os.path.basename(os.path.normpath(directory))
            remove_remote = input("Delete the remote GitHub repository as well? (y/n): ").strip().lower() == 'y'
            remove_git_repo(directory, repo_name, remove_remote=remove_remote)
        elif choice == '3':
            user = input("Enter the GitHub username: ").strip()
            repo_name = input("Enter the name of the repository to check: ").strip()
            exists = check_github_repo_exists(user, repo_name)
            if exists:
                print(colored(f"The repository '{user}/{repo_name}' exists on GitHub.", 'green'))
            else:
                print(colored(f"The repository '{user}/{repo_name}' does not exist on GitHub.", 'red'))
        elif choice == '4':
            prompt_additional_commits()
        elif choice == '5':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print(colored("Invalid choice. Please enter a number between 1 and 5.", 'red'))

if __name__ == "__main__":
    main()
