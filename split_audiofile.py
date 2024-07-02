from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence, detect_nonsilent
import os
import subprocess
import json

def get_audio_length(file_path):
    # Run ffprobe to get the file's duration
    command = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'json', file_path
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Parse the output
    result_json = json.loads(result.stdout)
    duration_seconds = float(result_json['format']['duration'])
    
    return duration_seconds

def my_detect_silence(audio_path, silence_thresh=-40, min_silence_len=1000, silence_chunk_len=100):
    print(f"About to read audio file {audio_path}")
    sound = AudioSegment.from_file(audio_path)
    print(f"Audio file read successfully {sound}")
    silence = detect_silence(sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    print(f"Returning silence segments {silence}")
    return silence

def split_audio_file(input_audio_path, chunk_length_sec=600, output_dir='chunks'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split the audio file into chunks using ffmpeg
    command = [
        'ffmpeg', '-i', input_audio_path,
        '-f', 'segment', '-segment_time', str(chunk_length_sec),
        '-c', 'copy', os.path.join(output_dir, 'chunk_%03d.mp3')
    ]
    subprocess.run(command)


if __name__ == "__main__":
    audio_path = "/workspaces/groqnotes-benjamin/downloads/audio/Session 03 AI⧸ML training for Trane Cohort 1.mp3"
    len=get_audio_length(audio_path)
    print(f"Audio length: {len}")
    #silence = my_detect_silence(audio_path)
    split_audio_file(audio_path)
    print(f"Silence detected in audio file: {silence}")