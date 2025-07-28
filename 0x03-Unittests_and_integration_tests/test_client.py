#!/usr/bin/env python3
"""
GithubOrgClient module
"""
import requests

def get_json(url: str) -> dict:
    """
    Fetches JSON from a given URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

class GithubOrgClient:
    """
    Client for Github Organization API.
    """
    def __init__(self, org_name: str):
        self._org_name = org_name

    def org(self) -> dict:
        """
        Returns the organization's payload.
        """
        return get_json(f"https://api.github.com/orgs/{self._org_name}")

    # You might have other methods here, but for this test, 'org' is sufficient.
