import subprocess

def video_to_audio_ogg(input_path: str, output_path: str):
    command = [
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-acodec", "libopus", output_path
    ]
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())