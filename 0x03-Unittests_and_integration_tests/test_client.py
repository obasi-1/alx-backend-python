#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient, get_json # Assuming client.py is in the same directory

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
        expected_payload = {"login": org_name, "id": 12345, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        # Configure the mock_get_json to return the expected_payload
        # when it's called.
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient with the current org_name
        org_client = GithubOrgClient(org_name)

        # Call the .org() method, which internally calls get_json
        result = org_client.org()

        # Construct the expected URL that get_json should have been called with
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that mock_get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result returned by org_client.org() matches
        # our expected_payload
        self.assertEqual(result, expected_payload)

if __name__ == '__main__':
    unittest.main()
