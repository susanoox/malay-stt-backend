from apiflask import APIBlueprint, Schema
from apiflask.fields import File, String, Boolean
from apiflask.validators import FileSize, FileType, OneOf
import uuid, datetime, json
from flask_cors import CORS

from helpers.run import convert_base64, srt_to_dict_list, run_file_generation, run_file_deletion
from helpers.runpod import stt_async, stt_sync
from helpers.constants import HOST_DOMAIN

stt_blueprint = APIBlueprint('STT', __name__, tag = 'Speech to Text APIs')
CORS(stt_blueprint)

class AudioFileUploadPayload(Schema):
    file = File(required=True, validate=[FileType(['.mp3', '.mp4', '.wav', '.ogg', '.flac', '.webm']), FileSize(max='100 MB')])
    model = String(required=True, default="large-v2", validate=OneOf(['base', 'medium', 'large-v2', 'large-v3']))
    translate = Boolean(required=False, default=True)
    enableVAD = Boolean(required=False, default=True)
    language = String(required=False, default=None)
    initialPrompt = String(required=False, default=None)

class RealTimeAudioStreamPayload(Schema):
    file = File(required=True, validate=[FileType(['.mp3', '.mp4', '.wav', '.ogg', '.flac', '.webm']), FileSize(max='100 MB')])
    model = String(required=False, default="large-v2", validate=OneOf(['base', 'medium', 'large-v2', 'large-v3']))
    translate = Boolean(required=False, default=True)
    enableVAD = Boolean(required=False, default=True)
    language = String(required=False, default=None)
    initialPrompt = String(required=False, default=None)

class RealTimeAudioStreamId(Schema):
    streamId = String(required=True)

@stt_blueprint.post('/stream')
@stt_blueprint.input(RealTimeAudioStreamPayload, location='form_and_files')
@stt_blueprint.input(RealTimeAudioStreamId, location='query')
def realtime_audio_stream(form_and_files_data, query_data):
    try: 
        streamId = query_data.get('streamId')
        audio_files = form_and_files_data['file']
        audio_base64 = convert_base64(audio_files)

        payload = {
            "model": form_and_files_data['model'],
            "translate": form_and_files_data['translate'],
            "transcription": 'srt',
            "enable_vad": form_and_files_data['enableVAD'],
            "initial_prompt": form_and_files_data['initialPrompt'],
            "language": form_and_files_data['language'] if form_and_files_data['language'] != "" else None,
            "audio_base64": audio_base64,
        }

        stt_output = stt_sync(payload)

        response = {
            "streamId" : streamId,
            "detected_language": stt_output['detected_language'],
            "transcription": srt_to_dict_list(stt_output['transcription']),
            "translation": srt_to_dict_list(stt_output['translation']) if form_and_files_data['translate'] else []
        }

        return response, 200

    except Exception as e:
        print(e)
        return { 'message': 'Internal server error. Please try again !' }, 500

@stt_blueprint.post('/upload')
@stt_blueprint.input(AudioFileUploadPayload, location='form_and_files')
def upload_audio_file(form_and_files_data):
    try: 
        audio_file = form_and_files_data['file']
        
        filename = run_file_generation(audio_file)

        audio_url = f"{HOST_DOMAIN}/api/v1/download?fileId={filename}"

        payload = {
            "audio": audio_url,
            "model": form_and_files_data['model'],
            "translate": form_and_files_data['translate'],
            "transcription": 'srt',
            "enable_vad": form_and_files_data['enableVAD'],
            "initial_prompt": form_and_files_data['initialPrompt'],
            "language": form_and_files_data['language'] if form_and_files_data['language'] != "" else None
        }

        stt_output = stt_async(payload)

        print('stt_output', stt_output)

        response = {
            "detected_language": stt_output['detected_language'],
            "transcription": srt_to_dict_list(stt_output['transcription']),
            "translation": srt_to_dict_list(stt_output['translation']) if form_and_files_data['translate'] else []
        }

        run_file_deletion(filename)

        return response, 200

    except Exception as e:
        print(e)
        return { 'message': 'Internal server error. Please try again !' }, 500
