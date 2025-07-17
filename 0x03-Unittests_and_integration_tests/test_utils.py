#!/usr/bin/env python3
"""TestAccessNestedMap class"""

import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Sequence, Mapping, Any, Callable
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """test class for NestedMap in utils module"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, output):
        """test case for output of access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), output)

    @parameterized.expand([
        ({}, ("a")),
        ({"a", 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        """test for KeyError exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """TestGetJson class implementation"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, test_url, test_payload):
        """test gets JSON call using mock using the request.get
        method"""
        with patch("requests.get") as mget:
            # assign the return value as JSON cause get_json uses json()
            # then on json() assign now the real data test_payload
            result = Mock()
            result.json.return_value = test_payload
            mget.return_value = result
            # call get_json
            response = get_json(test_url)
            # make sure get_json was called with test_url
            mget.assert_called_with(test_url)
            # assert the call result and our expected result
            self.assertEqual(response, test_payload)


class TestMemoize(unittest.TestCase):
    """TestMemoize class implementation"""
    def test_memoize(self):
        """test memoize function from utils"""
        class TestClass:
            """TestClass Implementation"""
            def a_method(self):
                """a_method implementation"""
                return 42

            @memoize
            def a_property(self):
                """a_property implementation"""
                return self.a_method()
        with patch.object(TestClass, "a_method") as m_a_method:
            m_a_method.return_value = 42
            foo = TestClass()
            foo_property_1 = foo.a_property
            foo_property_2 = foo.a_property
            # assert a method was called once
            m_a_method.assert_called_once()
            # assert even if called twice returns came value
            self.assertEqual(foo_property_1, 42)
            self.assertEqual(foo_property_2, 42)
