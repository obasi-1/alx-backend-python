#!/usr/bin/env python3
"""
Unit tests for the `client` module.
"""
import unittest
import requests # This import is not strictly needed for mocked tests but kept if original code had it
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock # Ensure Mock is imported
import sys
import os
from typing import Dict, List, Any # Ensure all types are imported

# Adjust sys.path to ensure client and utils can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

from client import GithubOrgClient
from utils import get_json # Import get_json for patching target

# Import fixtures
from fixtures import (TEST_PAYLOAD, org_payload,
                      repos_payload, expected_repos, apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """implementation of unitTests on methods in GithubOrgClient class
    """

    @parameterized.expand([("google",), ("abc",)]) # Ensure tuple format for parameterized
    @patch('client.get_json') # Patch get_json where it's used in client.py
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that `GithubOrgClient.org` returns the correct value
        and that `get_json` is called once with the expected argument.

        Args:
            org_name (str): The organization name for the test.
            mock_get_json (Mock): The mocked `get_json` function.
        """
        # Define the expected payload that get_json should return
        # This payload will be returned by the mocked get_json
        expected_payload = {"login": org_name, "id": 12345, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method under test (which calls get_json internally)
        result = client.org()

        # Construct the expected URL that get_json should be called with
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result of client.org() is the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url
        property with mocked org payload
        """
        expected_url = "https://api.github.com/orgs/test_org/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock):
        """Unit-test GithubOrgClient.public_repos
        with mocked get_json and _public_repos_url"""
        # Mocked payload for get_json
        mocked_repos_payload = [
            {"name": "google", "license": {"key": "mit"}},
            {"name": "facebook", "license": {"key": "apache-2.0"}}, # Changed to apache-2.0 for consistency
            {"name": "tesla", "license": {"key": "mit"}}
        ]
        
        # Patch the _public_repos_url property
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            # Mocking the property and method
            url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = url
            mock_get_json.return_value = mocked_repos_payload

            # Initialize the GithubOrgClient
            github_client = GithubOrgClient("google")

            # Call the method being tested
            repos = github_client.public_repos(license="mit")

            # Assertions
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(url)
            self.assertEqual(repos, ["google", "tesla"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, repo: Dict, license_key: str, output: bool):
        """test for has_license method for GithubOrgClient class
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, output)


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GitHub org client
    """
    @classmethod
    def setUpClass(cls):
        """Set up class for integration testing"""
        # Create the patcher for requests.get
        cls.get_patcher = patch('requests.get')
        # Start the patcher - mock_get will be used as the mock object
        cls.mock_get = cls.get_patcher.start()

        # Configure side effect to return different responses based on URL
        def side_effect(url: str):
            """Side effect function to mock json responses"""
            # Mock response object
            class MockResponse:
                def __init__(self, json_data: Any):
                    self._json_data = json_data

                def json(self) -> Any:
                    return self._json_data

            # Return appropriate fixtures based on the URL
            if url.endswith("/orgs/github"):
                return MockResponse(cls.org_payload)
            # This covers the repos_url call
            return MockResponse(cls.repos_payload)

        # Set the side effect on the mock object
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class after integration testing
        """
        # Stop the patcher
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method without a license
        """
        # Create an instance with GitHub as the org name
        github_client = GithubOrgClient("github")

        # Get the list of repositories
        repos = github_client.public_repos()

        # Check that the list of repositories is correct
        self.assertEqual(repos, self.expected_repos)

        # Verify that the mocked get was called correctly
        # It should be called twice: once for org(), once for _public_repos_url
        calls = [
            unittest.mock.call("https://api.github.com/orgs/github"),
            unittest.mock.call("https://api.github.com/orgs/github/repos")
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)


    def test_public_repos_with_license(self):
        """Test the public_repos method with a license argument
        """
        # Create an instance with GitHub as the org name
        github_client = GithubOrgClient("github")

        # Get the list of repositories with apache-2.0 license
        repos = github_client.public_repos(license="apache-2.0")

        # Check that the list of repositories is correct
        self.assertEqual(repos, self.apache2_repos)

        # Verify that the mocked get was called
        # It should be called twice: once for org(), once for _public_repos_url
        calls = [
            unittest.mock.call("https://api.github.com/orgs/github"),
            unittest.mock.call("https://api.github.com/orgs/github/repos")
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)

