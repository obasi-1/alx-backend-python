#!/usr/bin/env python3
"""
Unit tests for the `utils.access_nested_map` function.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Mapping, Sequence, Any


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
        
        # For the given inputs, the key that causes the error is the last
        # one in the path. We assert that the exception's argument is this key.
        self.assertEqual(cm.exception.args[0], path[-1])

