from pytube import YouTube
from tabulate import tabulate
import subprocess
import re
import shutil

video_url = input("Enter video URL:");
video_obj = YouTube(video_url);
print(
    'Title: ',video_obj.title,'\n'
    'Owner: ',video_obj.author,'\n'
    'Length:',video_obj.length,'seconds'
)

video_streams = list(enumerate(video_obj.streams.filter(only_video=True))) 
print("\nVideo Streams Fetching...")
stream_data = []
for index, stream in video_streams:
    mime_type_parts = stream.mime_type.split('/')
    file_extension = mime_type_parts[-1] if len(mime_type_parts) > 1 else ''
    stream_data.append([
        stream.itag,
        stream.resolution,
        file_extension,
        stream.filesize_mb
    ])
table_headers = ["itag", "Quality", "File Type", "Size"]
table = tabulate(stream_data, headers=table_headers, tablefmt="grid")
print(table)
itag = int(input("Enter itag: "))
downloading_src = video_obj.streams.get_by_itag(itag)

file_name = f"video.{downloading_src.mime_type.split('/')[-1]}"
downloading_src.download("Download",filename=file_name)

downloading_src = video_obj.streams.get_by_itag(251)
file_name = f"audio.{downloading_src.mime_type.split('/')[-1]}"
downloading_src.download("Download",filename=file_name)
print("Download complete!")


# file merging start
sanitized_title = re.sub(r'[^\w\s-]', '', video_obj.title)
sanitized_title = sanitized_title.replace(' ', '_')
command = f"ffmpeg -i Download\\video.mp4 -i Download\\audio.webm -c:v copy -c:a aac -strict experimental {sanitized_title}.mp4"
try:
    print("Converting...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    print(result.stdout)
    print(f"{sanitized_title} downloaded !")
except subprocess.CalledProcessError as e:
    print("Command error:\n", e.stderr)
    print("Full exception details:\n", e)

# delete directory
directory_path = 'Download'
try:
    shutil.rmtree(directory_path)
except Exception as e:
    print(f"An error occurred: {e}")