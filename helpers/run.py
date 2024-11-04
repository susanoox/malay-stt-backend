import base64
import re, os, uuid

from helpers.constants import TEMP_FOLDER

def convert_base64(audio_file):
    try:
        binary_file_data = audio_file.file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_output = base64_encoded_data.decode('utf-8')
        return base64_output
    
    except FileNotFoundError as e:
        print(f"Error while converting audio file into base64.\n{e}")
        return ''

def srt_to_dict_list(srt_text, translate=False):
    blocks = srt_text.strip().split("\n\n")
    transcription_list = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        timestamp_line = lines[1]
        text_lines = " ".join(lines[2:]).strip()

        match = re.search(r"(\d{2}:\d{2}:\d{2}),\d{3} --> (\d{2}:\d{2}:\d{2}),\d{3}", timestamp_line)

        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            timestamp = f"{start_time} --> {end_time}"

            if translate:
                transcription_list.append({
                    "timestamp": timestamp,
                    "translation": text_lines
                })
            else:
                transcription_list.append({
                    "timestamp": timestamp,
                    "transcription": text_lines
                })

    return transcription_list

def is_completed(status):
    return status in ["COMPLETED", "FAILED", "TIMED_OUT"]

def run_file_generation(file):
    try:
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(TEMP_FOLDER, filename)
        file.save(file_path)
        return filename

    except Exception as e:
        print(f"Error generating temp file: {e}")

def run_file_deletion(filename):
    try:
        file_path = os.path.join(TEMP_FOLDER, filename)
        os.remove(file_path)
        return True

    except FileNotFoundError as e:
        print(f"Error deleting temp file: {e}")
        return False