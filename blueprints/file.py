from apiflask import APIBlueprint, Schema
from apiflask.fields import String
from flask_cors import CORS
from flask import send_from_directory

from helpers.run import convert_base64, srt_to_dict_list
from helpers.constants import TEMP_FOLDER

file_blueprint = APIBlueprint('FILES', __name__, tag = 'Share audio files')
CORS(file_blueprint)

class FileId(Schema):
    fileId = String(required=True)

@file_blueprint.get('/download')
@file_blueprint.input(FileId, location='query')
def download_file(query_data):
    fileId = query_data.get('fileId')
    return send_from_directory(TEMP_FOLDER, fileId)