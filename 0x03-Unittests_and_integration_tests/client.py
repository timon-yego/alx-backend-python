import requests

def get_json(url):
    """Make a GET request and return the JSON response."""
    response = requests.get(url)
    return response.json()

class GithubOrgClient:
    """A client to interact with GitHub organization APIs."""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch and return the organization data."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
