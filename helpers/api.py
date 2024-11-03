import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url, api_key, endpoint_id):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"{api_key}",
            "content-type": "application/json"
        }
        self.endpoint_id = endpoint_id

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[408, 429])
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _request(self, method, endpoint, payload=None, timeout = 10):
        url = f"{self.base_url}/{self.endpoint_id}/{endpoint}"
        response = self.session.request(method, url, headers=self.headers, json=payload, timeout=timeout)

        if response.status_code == 401:
            print('Error due to authorised request to runpod.io')

        response.raise_for_status()
        return response.json()

    def post(self, endpoint, payload, timeout=10):
        return self._request("POST", endpoint, payload, timeout)

    def get(self, endpoint, timeout=10):
        return self._request("GET", endpoint, timeout)