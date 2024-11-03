import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import RequestException

class AxiosInstance:
    def __init__(self, base_url, api_key, endpoint_id):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"{api_key}",
            "content-type": "application/json"
        }
        self.endpoint_id = endpoint_id

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier=1, min=3, max=3),
        retry = retry_if_exception_type(RequestException)
    )
    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier=1, min=3, max=3),
        retry = retry_if_exception_type(RequestException)
    )
    def post(self, endpoint, payload):
        url = f"{self.base_url}/{self.endpoint_id}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


base_url = "https://api.runpod.ai/v2"
api_key = "H9V38JP8JT5TOWYA7MPK6K3QOSGWUW24Q1PILX38"
endpoint_id = "jmtz1y3f5ymhsp"
endpoint = "runsync"
input_data = {
    "input": {
        "audio": "https://github.com/runpod-workers/sample-inputs/raw/main/audio/gettysburg.wav"
    }
}

axios_instance = AxiosInstance(base_url, api_key, endpoint_id)
response = axios_instance.post(endpoint, input_data)
print(response)