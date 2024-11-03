import runpod
import os, time
from dotenv import load_dotenv

from helpers.api import APIClient
from helpers.run import is_completed

load_dotenv()

runpod_api_key = os.getenv("RUNPOD_APIKEY")
runpod_endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")
runpod_baseurl = os.getenv("RUNPOD_BASEURL")

runpod.api_key = runpod_api_key

def stt_sync(payload): # less than 30 sec
    try:
        endpoint = runpod.Endpoint(runpod_endpoint_id)
        run_request = endpoint.run_sync(payload, 60)
        return run_request

    except Exception as e:
        print(f'Error while generating sync audio transcription\n {e}')
        return {}
    
def get_job_state(job_id):
    client_instance = APIClient(runpod_baseurl, runpod_api_key, runpod_endpoint_id)
    client_response = client_instance.get(f'status/{job_id}')
    
    return client_response

def stt_async(payload, timeout=10): # more than 30 sec
    try:
        client_instance = APIClient(runpod_baseurl, runpod_api_key, runpod_endpoint_id)
        client_response = client_instance.post('run', { "input": payload })

        job_id = client_response['id']

        if is_completed(client_response["status"]):
            return client_response.get("output", {})

        while True:
            job_state = get_job_state(job_id)
            job_status = job_state.get('status')

            if is_completed(job_status):
                return job_state.get('output', {})

            elif job_status in ["FAILED"]:
                print(f'Job Id [{job_id}] failed or encountered an error.')
                return {}

            else:
                print(f'Job Id [{job_id}] in queue or processing. Waiting 5 seconds...')
                time.sleep(5)
            
    except Exception as e:
        print(f'Error while generating async audio transcription\n {e}')
        return {}
