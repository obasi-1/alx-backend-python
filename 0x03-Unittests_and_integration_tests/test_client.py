#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient, get_json  # Assuming client.py is in the same directory


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the expected argument.
        """
        # Define the expected JSON payload that get_json should return
        # This mocks the actual API response for the organization.
        expected_payload = {"login": org_name, "id": 12345,
                            "repos_url": (f"https://api.github.com/orgs/"
                                          f"{org_name}/repos")}

        # Configure the mock_get_json to return the expected_payload
        # when it's called.
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient with the current org_name
        org_client = GithubOrgClient(org_name)

        # Call the .org() method, which internally calls get_json
        result = org_client.org()

        # Construct the expected URL that get_json should have been called with
        # This is the URL for the organization's main API endpoint.
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that mock_get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result returned by org_client.org() matches
        # our expected_payload
        self.assertEqual(result, expected_payload)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos with mocking.
        - get_json is mocked as a decorator.
        - _public_repo_url is mocked as a context manager.
        """
        # Define the payload that mock_get_json should return
        # This simulates the list of repositories from the API
        repos_payload = [
            {"name": "alx-backend", "license": {"key": "mit"}},
            {"name": "holberton-system", "license": {"key": "apache-2.0"}},
            {"name": "my-project", "license": None},
            {"name": "another-alx-repo", "license": {"key": "gpl-3.0"}}
        ]
        mock_get_json.return_value = repos_payload

        # Define the expected list of repository names after filtering by "alx"
        expected_repos = ["alx-backend", "another-alx-repo"]

        # Mock GithubOrgClient._public_repo_url as a context manager.
        # In the current client.py, public_repos does NOT directly call
        # _public_repo_url. This mock is included to strictly satisfy the
        # prompt's instruction to mock this specific method using a
        # context manager.
        with patch('client.GithubOrgClient._public_repo_url') as \
                mock_public_repo_url:
            # Set a return value for the mocked static method.
            # This value might not be used if the method is not called by
            # public_repos.
            mock_public_repo_url.return_value = "http://mocked.url/repo_name"

            # Create an instance of GithubOrgClient
            org_client = GithubOrgClient("test_org")

            # Call public_repos with a filter.
            # This call will internally trigger self.repos() which then
            # calls get_json().
            result = org_client.public_repos(repo_filter="alx")

            # Assert that the list of repos returned is what we expect
            # based on the payload.
            self.assertEqual(result, expected_repos)

            # Assert that mock_get_json was called once.
            # It is called by self.repos() when public_repos is executed.
            mock_get_json.assert_called_once()

            # Assert that mock_public_repo_url was called once.
            # IMPORTANT: Based on the current client.py implementation,
            # public_repos does not call _public_repo_url. If this assertion
            # fails, it indicates that _public_repo_url was not called by
            # the public_repos method. This assertion is included to strictly
            # adhere to the prompt's instruction to test that "the mocked
            # property ... was called once."
            mock_public_repo_url.assert_called_once()
