#!/usr/bin/env python3
"""
Unit tests for the `client` module.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import sys
import os
from typing import Dict

# Adjust sys.path to ensure client and utils can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

from client import GithubOrgClient
from utils import get_json # Import get_json for patching target


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
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
        expected_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method under test
        result = client.org()

        # Construct the expected URL that get_json should be called with
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result of client.org() is the expected payload
        self.assertEqual(result, expected_payload)

