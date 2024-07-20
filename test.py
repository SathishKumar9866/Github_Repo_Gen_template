

import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from CRUD.util import load_config, run_command
from CRUD.git import gh_authenticate, clone_repo, initialize_git_repo, git_add_commit_push
from CRUD.create import  create_dockerfile, create_github_repo, create_gitignore, create_readme, create_repo_and_commit, create_requirements
from CRUD.delete import remove_git_repo,delete_github_repo

# ANSI escape codes for colored output
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


class TestCRUDOperations(unittest.TestCase):
    @patch('CRUD.util.load_config')
    # @patch('CRUD.git.gh_authenticate')
    # def test_authentication(self, mock_gh_authenticate, mock_load_config):
    #     mock_load_config.return_value = {'github_user': 'sathishpaloju', 'repo_name': 'test_directory'}
    #     gh_authenticate()
    #     mock_gh_authenticate.assert_called_once()

    @patch('CRUD.git.clone_repo')
    @patch('CRUD.git.initialize_git_repo')
    @patch('CRUD.create.create_readme')
    @patch('CRUD.create.create_requirements')
    @patch('CRUD.create.create_dockerfile')
    @patch('CRUD.create.create_gitignore')
    @patch('CRUD.git.git_add_commit_push')
    def test_initial_commit(self, mock_git_add_commit_push, mock_create_gitignore, mock_create_dockerfile, mock_create_requirements, mock_create_readme, mock_initialize_git_repo, mock_clone_repo):
        config = {
            'github_user': 'sathishpaloju',
            'repo_name': 'test_directory',
            'dependencies': ['dependency1', 'dependency2'],
            'python_version': '3.9'
        }
        clone_repo(config['github_user'], config['repo_name'])
        initialize_git_repo(config['repo_name'])
        create_readme(config['repo_name'])
        create_requirements(config['dependencies'])
        create_dockerfile(config['repo_name'], config['python_version'])
        create_gitignore()
        git_add_commit_push()

        mock_clone_repo.assert_called_once_with(config['github_user'], config['repo_name'])
        mock_initialize_git_repo.assert_called_once_with(config['repo_name'])
        mock_create_readme.assert_called_once_with(config['repo_name'])
        mock_create_requirements.assert_called_once_with(config['dependencies'])
        mock_create_dockerfile.assert_called_once_with(config['repo_name'], config['python_version'])
        mock_create_gitignore.assert_called_once()
        mock_git_add_commit_push.assert_called_once()

    @patch('CRUD.create.create_repo_and_commit')
    def test_create_repo_and_commit_directory(self, mock_create_repo_and_commit):
        directory = 'kickstarter'
        create_repo_and_commit(directory)
        mock_create_repo_and_commit.assert_called_once_with(directory, delete_if_exists=False)

    





if __name__ == '__main__':
    unittest.main()
