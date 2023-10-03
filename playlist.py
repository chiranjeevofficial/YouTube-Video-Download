from pytube import YouTube
from pytube import Playlist
import subprocess
import re
import shutil


url = input("Enter Playlist URL: ")
playlist = Playlist(url)
print(playlist.title)

for video in playlist.videos:
    print(video.title)
    print("Downloading...")
    downloading_src = video.streams.get_by_itag(137)
    file_name = f"video.{downloading_src.mime_type.split('/')[-1]}"
    downloading_src.download("Download",filename=file_name)
    downloading_src = video.streams.get_by_itag(251)
    file_name = f"audio.{downloading_src.mime_type.split('/')[-1]}"
    downloading_src.download("Download",filename=file_name)

    # file merging start
    sanitized_title = re.sub(r'[^\w\s-]', '', video.title)
    sanitized_title = sanitized_title.replace(' ', '_')
    command = f"ffmpeg -i Download\\video.mp4 -i Download\\audio.webm -c:v copy -c:a aac -strict experimental {sanitized_title}.mp4"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Command error:\n", e.stderr)
        print("Full exception details:\n", e)

    # delete directory
    directory_path = 'Download'
    try:
        shutil.rmtree(directory_path)
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Download complete!")
