import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio

# Input and output folder paths
input_folder = r"C:\Users\vesga\Documentos\Victor\Codin_projects\AutoTikTok\videos"  # Replace with the path to your input folder containing MP4 files
output_folder = r"C:\Users\vesga\Documentos\Victor\Codin_projects\AutoTikTok\Audios"  # Replace with the path to your output folder for MP3 files

# Ensure the output folder exists, or create it if it doesn't
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all files in the input folder
input_files = os.listdir(input_folder)

# Filter the list to include only MP4 files
mp4_files = [f for f in input_files if f.endswith(".mp4")]

# Loop through each MP4 file and convert it to MP3
for mp4_file in mp4_files:
    # Construct the full paths for input and output files
    input_path = os.path.join(input_folder, mp4_file)
    mp3_file = mp4_file[:-4] + ".mp3"  # Change the file extension to .mp3
    output_path = os.path.join(output_folder, mp3_file)

    # Convert MP4 to MP3
    ffmpeg_extract_audio(input_path, output_path)

print("Conversion complete.")
