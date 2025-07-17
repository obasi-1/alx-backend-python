#!/usr/bin/env python3
"""
A module for interacting with the GitHub API.
"""
from utils import get_json
from typing import Dict

class GithubOrgClient:
    """
    A client for interacting with the GitHub Organizations API.
    """
    def __init__(self, org_name: str) -> None:
        """
        Initializes a GithubOrgClient instance.

        Args:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name

    def org(self) -> Dict:
        """
        Retrieves the organization's information from the GitHub API.

        Returns:
            Dict: A dictionary containing the organization's data.
        """
        # Construct the URL for the organization's API endpoint
        url = f"https://api.github.com/orgs/{self._org_name}"
        # Use the get_json utility to fetch and parse the data
        return get_json(url)

