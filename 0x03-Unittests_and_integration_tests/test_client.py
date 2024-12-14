#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Assuming the client module contains the GithubOrgClient class

class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org, mock_get_json):
        # Mock the response of get_json
        mock_get_json.return_value = {"org": org}
        
        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org)
        
        # Call the org method
        result = client.org()
        
        # Check that get_json was called once with the correct argument
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")
        
        # Check that the result is as expected
        self.assertEqual(result, {"org": org})

if __name__ == '__main__':
    unittest.main()
