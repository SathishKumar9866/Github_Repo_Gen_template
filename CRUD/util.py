import subprocess
import yaml
from termcolor import colored

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if result.stdout:
            print("Command output:", result.stdout)
        if result.stderr:
            print("Command error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}':")
        if e.stdout:
            print("Command output:", e.stdout)
        if e.stderr:
            print("Command error:", e.stderr)

def prompt_additional_commits():
    while True:
        response = input(colored("Do you want to add another commit? (y/n): ", 'yellow')).strip().lower()
        if response == 'y':
            files_to_add = input(colored("Enter the files to add (space-separated): ", 'yellow')).strip()
            commit_message = input(colored("Enter the commit message: ", 'yellow')).strip()
            run_command(f'git add {files_to_add}')
            run_command(f'git commit -m "{commit_message}"')
            run_command('git push')
        elif response == 'n':
            break
        else:
            print(colored("Invalid response. Please enter 'y' or 'n'.", 'red'))