# Create the client.py file with the provided content
%%writefile client.py
#!/usr/bin/env python3
"""
A module for the GithubOrgClient class.
"""
import requests
from functools import wraps

def get_json(url: str) -> dict:
    """
    Fetches JSON data from a given URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

class GithubOrgClient:
    """
    Client for interacting with the GitHub API for organizations.
    """
    def __init__(self, org_name: str):
        self._org_name = org_name

    def org(self) -> dict:
        """
        Returns the organization's information.
        """
        url = f"https://api.github.com/orgs/{self._org_name}"
        return get_json(url)

    def repos_url(self) -> str:
        """
        Returns the URL for the organization's repositories.
        """
        return self.org()["repos_url"]

    def repos(self) -> list:
        """
        Returns a list of repositories for the organization.
        """
        url = self.repos_url()
        return get_json(url)

    def public_repos(self, repo_filter: str = None) -> list:
        """
        Returns a list of public repositories, optionally filtered.
        """
        repos = self.repos()
        if repo_filter:
            return [repo["name"] for repo in repos if repo_filter in repo["name"]]
        return [repo["name"] for repo in repos]

    @staticmethod
    def _public_repo_url(name: str) -> str:
        """
        Returns the URL for a public repository.
        """
        return f"https://github.com/{name}"

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """
        Checks if a repository has a specific license.
        """
        if "license" in repo and repo["license"] is not None:
            return repo["license"]["key"] == license_key
        return False
