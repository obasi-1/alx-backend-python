#!/usr/bin/env python3
"""
Unit tests for the utils.py module, specifically for the get_json function.
"""
import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the parent directory to the sys.path to allow importing utils
# This is important if test_utils.py is in a subdirectory relative to utils.py
# Adjust this path if utils.py is in a different location relative to test_utils.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Assuming utils.py is in the same directory or accessible via PYTHONPATH
import utils

class TestGetJson(unittest.TestCase):
    """
    Tests for the utils.get_json function.
    """

    @patch('requests.get')
    def test_get_json(self, mock_get: Mock):
        """
        Tests that utils.get_json returns the expected result by mocking
        requests.get.

        It verifies:
        - requests.get is called exactly once with the correct URL.
        - The output of get_json matches the mocked payload.
        """
        # Define the test cases as a list of tuples: (test_url, test_payload)
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            with self.subTest(url=test_url, payload=test_payload):
                # Configure the mock object for each subtest
                # Create a mock response object
                mock_response = Mock()
                # Set the return value of the .json() method on the mock response
                mock_response.json.return_value = test_payload
                # Configure the requests.get mock to return our mock response
                mock_get.return_value = mock_response

                # Call the function under test
                result = utils.get_json(test_url)

                # Assert that requests.get was called exactly once with the correct URL
                mock_get.assert_called_once_with(test_url)

                # Assert that the output of get_json is equal to test_payload
                self.assertEqual(result, test_payload)

                # Reset the mock for the next iteration of the loop
                # This is crucial when using a loop with assert_called_once
                mock_get.reset_mock()

if __name__ == '__main__':
    unittest.main()

