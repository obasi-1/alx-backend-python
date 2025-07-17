#!/usr/bin/env python3
"""TestGithubOrgClient class implementation
"""

import unittest
import requests
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import (TEST_PAYLOAD, org_payload,
                      repos_payload, expected_repos, apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """implementation of unitTests on methods in GithubOrgClient class
    """

    @parameterized.expand([("google"), ("abc")])
    @patch.object(GithubOrgClient, "org")
    def test_org(self, org_name, mock_org):
        """test implementation for the org method"""
        url = f"https://api.github.com/orgs/{org_name}"
        fake_dict = {"company": org_name}
        mock_org.return_value = fake_dict

        new_company = GithubOrgClient(org_name)
        new_comp_info = new_company.org()
        mock_org.assert_called_once_with()

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
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos
        with mocked get_json and _public_repos_url"""
        # Mocked payload for get_json
        mocked_payload = [
            {"name": "google", "license": {"key": "mit"}},
            {"name": "facebook", "license": {"key": "apache"}},
            {"name": "tesla", "license": {"key": "mit"}}
        ]
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            # Mocking the property and method
            url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = url
            mock_get_json.return_value = mocked_payload

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
    def test_has_license(self, repo, license_key, output):
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
        def side_effect(url):
            """Side effect function to mock json responses"""
            # Mock response object
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data

                def json(self):
                    return self._json_data

            # Return appropriate fixtures based on the URL
            if url.endswith("/orgs/github"):
                return MockResponse(cls.org_payload)
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
    self.mock_get.assert_called()


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
    self.mock_get.assert_called()
