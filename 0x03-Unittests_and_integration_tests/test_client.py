#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=MagicMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct value.
        """
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=MagicMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that public_repos returns the expected list of repositories.
        """
        mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly identifies if a repo has a specific license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)

@parameterized_class([
    {"org_payload": org_payload, 
     "repos_payload": repos_payload, 
     "expected_repos": expected_repos, 
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class by patching requests.get to mock external API calls.
        """
        cls.get_patcher = patch('requests.get')

        # Start the patcher and get a reference to the mocked get
        cls.mock_get = cls.get_patcher.start()

        # Define side_effect to return the correct fixture based on the URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MagicMock(json=lambda: cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MagicMock(json=lambda: cls.repos_payload)
            return MagicMock(json=lambda: None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class by stopping the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns the expected repositories.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos filters repos by license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)

if __name__ == "__main__":
    unittest.main()



if __name__ == '__main__':
    unittest.main()
