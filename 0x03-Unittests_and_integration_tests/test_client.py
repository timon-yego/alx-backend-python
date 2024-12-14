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

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org):
        # Define a known payload that would be returned by the org property
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
        
        # Create an instance of GithubOrgClient with the 'google' organization
        client = GithubOrgClient("google")
        
        # Call the _public_repos_url property
        result = client._public_repos_url
        
        # Assert that the repos_url in the org payload is correctly used in the result
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

if __name__ == '__main__':
    unittest.main()