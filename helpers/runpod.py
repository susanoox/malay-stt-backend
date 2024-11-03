import runpod
import os
from dotenv import load_dotenv

load_dotenv()

runpod.api_key = os.getenv("RUNPOD_APIKEY")
runpod_endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")

def stt_sync(payload): # less than 30 sec
    try:
        endpoint = runpod.Endpoint(runpod_endpoint_id)
        run_request = endpoint.run_sync(payload, 60)
        return run_request
    except Exception as e:
        print(f'Error while generating sync audio transcription\n {e}')

async def stt_async(payload): # more than 30 sec
    pass
