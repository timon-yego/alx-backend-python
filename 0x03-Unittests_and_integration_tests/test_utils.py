#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function in utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """
        Test access_nested_map returns the expected result for various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # Empty dictionary, key "a" not found
        ({"a": 1}, ("a", "b")),  # Key "b" not found under "a"
    ])

    def test_access_nested_map_exception(self, nested_map: dict, path: tuple) -> None:
        """
        Test that KeyError is raised when a path does not exist in the nested_map.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        
        # Verify that the exception message matches the path that caused the KeyError
        self.assertEqual(str(cm.exception), repr(path))



if __name__ == "__main__":
    unittest.main()
