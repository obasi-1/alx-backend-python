#!/usr/bin/env python3
"""
Unit tests for the `utils` module.
"""
import unittest
from unittest.mock import patch, Mock
import sys
import os
from typing import Mapping, Sequence, Any, Dict

# Adjust sys.path to ensure utils can be imported if test_utils.py is in a
# subdirectory. This must be at the top of the file after docstrings.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

# Import functions from utils.py
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Tests that `access_nested_map` returns the expected result
        for various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence
    ) -> None:
        """
        Tests that a KeyError is raised for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        
        # Verify that the KeyError message matches the last key in the path
        self.assertEqual(cm.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """
    Test suite for the `get_json` function with mocked HTTP calls.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')  # Patch requests.get within the utils module
    def test_get_json(self, test_url: str, test_payload: Dict,
                       mock_get: Mock) -> None:
        """
        Tests that get_json returns the expected result by mocking HTTP calls.
        It ensures that the requests.get method is called exactly once with the
        correct URL and that the function's output matches the specified
        payload.
        """
        # Configure the mock to return a response object with a specific
        # json payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert that the mocked get method was called exactly once with the
        # correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test suite for the `memoize` decorator.
    """
    def test_memoize(self) -> None:
        """
        Tests that the memoize decorator correctly caches the result
        of a method call and prevents subsequent calls to the original method.
        """
        class TestClass:
            """
            A simple class to demonstrate memoization.
            """
            def a_method(self):
                """
                A method that returns a fixed value.
                This method will be mocked to track calls.
                """
                return 42

            @memoize
            def a_property(self):
                """
                A property that uses the memoize decorator.
                It calls a_method internally.
                """
                return self.a_method()

        # Patch 'a_method' within the TestClass instance
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            test_instance = TestClass()

            # Call a_property twice
            result1 = test_instance.a_property()
            result2 = test_instance.a_property()

            # Assert that a_method was called exactly once
            mock_a_method.assert_called_once()

            # Assert that the correct result is returned
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    unittest.main()
