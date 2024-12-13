#!/usr/bin/env python3
"""
Test suite for utils.access_nested_map.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),  # Key exists
        ({"a": {"b": 2}}, ("a",), {"b": 2}),  # Nested dict returned
        ({"a": {"b": 2}}, ("a", "b"), 2),  # Deep key exists
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # Empty dict, key not found
        ({"a": 1}, ("a", "b")),  # Key exists, but subkey does not
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Ensure exception message matches the missing key
        self.assertEqual(str(cm.exception), repr(path))

        
if __name__ == "__main__":
    unittest.main()