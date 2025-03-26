import os
import subprocess

def get_video_frame_count(input_file):
    # First try to get the number of frames from the metadata
    command_metadata = [
        ffprobe_path, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_frames',
        '-of', 'default=noprint_wrappers=1', input_file
    ]
    result_metadata = subprocess.run(command_metadata, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result_metadata.returncode == 0:
        # If nb_frames is available in the metadata
        try:
            frame_count = result_metadata.stdout.strip().split('=')[1]  # Get the value after '='
            if str(frame_count).isnumeric() == True:
                return int(frame_count)
            else:
                pass
        except IndexError:
            pass  # Handle case where nb_frames isn't present or parsable
    
    # If no frame count found or error, fallback to counting frames method
    command_count_frames = [
        ffprobe_path, '-v', 'error', '-select_streams', 'v:0',
        '-count_frames', '-show_entries', 'stream=nb_read_frames',
        '-of', 'default=noprint_wrappers=1', input_file
    ]
    
    result_count_frames = subprocess.run(command_count_frames, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result_count_frames.returncode == 0:
        # Extract the number of frames from the output string
        frame_count = result_count_frames.stdout.strip().split('=')[1]  # Get the value after '='
        return int(frame_count)
    else:
        raise Exception(f"Error in ffprobe: {result_metadata.stderr or result_count_frames.stderr}")

ffprobe_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffprobe.exe')

my_file_list = []
my_dir = os.getcwd()
for my_file in os.listdir(my_dir):
    if os.path.isfile(my_file):
        print(str(my_file))
        my_file_list.append(my_file)

total_frames_in_chunks = 0
for video_file in my_file_list:
    try:
        frames_processed = int(get_video_frame_count(video_file))
        total_frames_in_chunks += frames_processed
    except:
        print("One or more chunks could not be processed")
        break

print("TOTAL FRAMES IN ALL CHUNKS: " + str(total_frames_in_chunks))

