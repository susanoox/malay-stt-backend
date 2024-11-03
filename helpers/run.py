import base64
import re

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