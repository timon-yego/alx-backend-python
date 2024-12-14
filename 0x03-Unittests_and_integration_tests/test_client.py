#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for GithubOrgClient class.
    """

    @patch('client.GithubOrgClient.get_json')  # Mocking the get_json method
    def test_org(self, mock_get_json):
        """
        Test the org method of GithubOrgClient.
        """
        # Simulate a payload that would be returned by get_json
        mock_get_json.return_value = {"login": "google", "id": 1234}

        client = GithubOrgClient("google")
        org_data = client.org()

        # Assert that the org method returns the correct value
        self.assertEqual(org_data, {"login": "google", "id": 1234})
        # Verify that get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(
                                    "https://api.github.com/orgs/google")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_has_license(self, repo, license_key,
                         expected_result, mock_get_json):
        """
        Test the has_license method of GithubOrgClient.
        Parametrize the test with different repo license and expected results.
        """
        # Mock the get_json method to return the repo with 'license' key
        mock_get_json.return_value = repo

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("google")

        # Call the has_license method
        result = client.has_license(license_key)

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

        # Verify that get_json was called once
        mock_get_json.assert_called_once_with(
                                "https://api.github.com/orgs/google/repos")

    @patch('client.GithubOrgClient.get_json')
    @patch('client.GithubOrgClient._public_repos_url')
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient.
        """
        # Define a sample payload for the mocked response of get_json
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("google")

        # Call the public_repos method
        repos = client.public_repos()

        # Assert that the returned list of repos is as expected
        self.assertEqual(repos, [{"name": "repo1"}, {"name": "repo2"}])

        # Assert that mocked property and mocked get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
                            "https://api.github.com/orgs/google/repos")

    @patch('client.GithubOrgClient.get_json')
    @patch('client.GithubOrgClient._public_repos_url')
    def test_public_repos_url(self, mock_public_repos_url, mock_get_json):
        """
        Test the _public_repos_url method of GithubOrgClient.
        """
        # Define a sample payload
        mock_get_json.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"}
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("google")

        # Assert that the _public_repos_url property is used correctly
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

        # Assert mocked property and mocked get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
                            "https://api.github.com/orgs/google/repos")


if __name__ == '__main__':
    unittest.main()
