"""
videoChunker.py

Written by Zack Mason on 9/4/2024

This application allows a user to perform a number of operations on a local
video file.

Currently it can be run as a standalone application via conversion to .exe
or it can be run as a python script. If run as the latter, you will need
to have FFMPEG installed in the working directory. This script uses a 
hardcoded relative path to ffmpeg for ease of use in executable form.
Check the script for this path if intending to use as a python application.
Actually, here it is: ffmpeg_path = os.path.join(os.path.dirname(__file__),
   'ffmpeg', 'ffmpeg.exe')

1. Chunking
- The user can upload a video file to chunk it into smaller files based on
  size and length. Basically, the user will be given the video size in GB
  per minute and then they are able to specify how long (in seconds) they
  would like each chunk of video to be.

2. Converting
- The user is able to convert their video file into .mov or .mp4 formats.
- This application will work with other video file formats but we are 
  only interested in converting to these two formats as of right now.

3. Metadata entry and generation
- This application allows the user to input metadata and generate a 
  .CSV metadata file that contains their responses.
"""

import os
import csv
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import END
from tkinter import filedialog
import threading
import datetime
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import ffmpeg
import json

# Use relative path to the ffmpeg executable as it's being bundled into an exe
ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
ffprobe_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffprobe.exe')
selected_files = []
selected_directory = ""
# Update the path to ffmpeg in the ffmpeg-python library
ffmpeg._ffmpeg_exe = ffmpeg_path
ffmpeg._ffprobe_exe = ffprobe_path

def on_option_change(*args):
    """
    Handles changes in the selection of a dropdown menu.

    This function is triggered when the user selects a different option from a
    dropdown menu. It retrieves the currently selected option, prints it to the
    console, and returns the selected option.

    Parameters:
    *args: Variable length argument list that captures any additional arguments
    passed to the function (typically used in event handlers).

    Returns:
    str: The currently selected option from the dropdown menu.

    Side Effects:
    - Prints the selected option to the console.

    Notes:
    - The `option_var` variable should be a Tkinter `StringVar` or similar
      variable that is associated with the dropdown menu to track the selected
      option.
    - This function is typically used as a callback for events related to
      changes in the dropdown menu selection.
    """
    selected_option = option_var.get()
    print(f"Selected option: {selected_option}")
    return selected_option

def video_operation():
    """
    Initiates the video splitting process based on user input.

    This function performs the following actions:
    1. Retrieves the file path of the video from the user input.
    2. Checks if the specified file exists.
        - If the file does not exist, displays an informational message to
          the user to re-enter a valid file path.
        - If the file exists, starts a background thread to execute the
          video splitting operation using the `split_video` function with
          the provided video file path and segment length.
    3. Displays an informational message to indicate that the video
       splitting operation has started and advises the user not to click
       the split button again until the operation is complete.

    Parameters:
    None

    Returns:
    None

    Side Effects:
    - Shows a message box if the file does not exist or if the video
      splitting operation has started.
    - Starts a background thread for video splitting, allowing the main
      thread to remain responsive.

    Notes:
    - The `videoFileNameEntry` should be a Tkinter entry widget where
      the user inputs the path to the video file.
    - The `chunkLengthEntry` should be a Tkinter entry widget where the
      user specifies the segment length for the video chunks.
    - Ensure that `threading` is imported and used to run the video
      splitting operation in a separate thread to avoid blocking the main
      thread.
    """

    video_file_path_string = videoFileNameEntry.get()
    video_file_path_list = [item.strip() for item in video_file_path_string.split(',')]

    file_name_update_string = updated_file_name_entry.get()
    file_name_update_list = [item.strip() for item in file_name_update_string.split(',')]
    
    output_directory_updated = output_directory_entry.get()

    i=0
    file_name_dict = {}
    for video_file_path in video_file_path_list:
        try:
            temp_dict = {video_file_path:file_name_update_list[i]}
        except:
            temp_dict = {video_file_path:video_file_path}
        i+=1
        file_name_dict.update(temp_dict)

    for video_file_path in video_file_path_list:
        print("Looking for this: " + video_file_path)
        file_exists = os.path.isfile(video_file_path)
        if not file_exists:
            messagebox.showerror("File not found",
                "The file specified does not exist. Re-enter a file path")
            return None
        else:
            segment_length = chunkLengthEntry.get()
            #if len(str(segment_length))<1:
            #    messagebox.showerror("Missing Information",
            #        "Enter the desired length for your video segments.")
            #    return None
            #else:
            threading.Thread(target=split_video, args=(video_file_path,
                segment_length, file_name_dict, update_progress)).start()

def submit_data():
    """
    Collects data from multiple input fields and saves it to a CSV file.

    This function performs the following actions:
    1. Retrieves data from 23 input fields.
    2. Checks if a CSV file named 'metadata.csv' already exists in the working
       directory.
    3. Opens the CSV file in append mode and writes the data collected from the input
       fields.
        - If the file does not exist, it writes headers to the CSV file before appending
          the data.
    4. Displays a message box to inform the user that the data has been successfully
       saved.
    5. Clears all the input fields after submission to prepare for the next entry.

    Parameters:
    None

    Returns:
    None

    Side Effects:
    - Appends data to 'metadata.csv' or creates the file if it does not exist.
    - Displays a message box confirming the successful saving of data.
    - Clears the contents of all input fields.

    Notes:
    - The function assumes that `entry1`, `entry2`, ..., `entry23` are Tkinter `Entry`
      widgets from which the data is retrieved.
    - The CSV file is encoded in UTF-8 and uses newline characters to separate rows.
    - Ensure that the `csv` and `tkinter.messagebox` modules are imported and available
      for the function to operate correctly.
    """
    field1_data = entry1.get()
    field2_data = entry2.get()
    field3_data = entry3.get()
    field4_data = entry4.get()
    field5_data = entry5.get()
    field6_data = entry6.get()
    field7_data = entry7.get()
    field8_data = entry8.get()
    field9_data = entry9.get()
    field10_data = entry10.get()
    field11_data = entry11.get()
    field12_data = entry12.get()
    field13_data = entry13.get()
    field14_data = entry14.get()
    field15_data = entry15.get()
    field16_data = entry16.get()
    field17_data = entry17.get()
    field18_data = entry18.get()
    field19_data = entry19.get()
    field20_data = entry20.get()
    field21_data = entry21.get()
    field22_data = entry22.get()
    field23_data = entry23.get()

    requiredFields = [field1_data,field2_data,field3_data,field4_data,field5_data,
        field6_data,field7_data,field8_data,field13_data,field15_data,field16_data,
        field17_data,field18_data,field19_data,field20_data,field21_data,field22_data,
        field23_data]
    for myData in requiredFields:
        if len(str(myData))<1:
            messagebox.showerror("Required Fields Incomplete",
            "Please fill in all required fields. These are bolded and marked"+
            " with asterisks.")
            return None

    filename = 'metadata.csv' # File name for the CSV
    file_exists = os.path.isfile(filename) # Check if the file exists
    # Open the CSV file for appending new metadata
    with open(filename, mode='a', newline='',encoding="UTF-8") as file:
        writer = csv.writer(file)
        if not file_exists: # Write headers if the file doesn't exist.
            writer.writerow(["Project ID (or CruiseID)", "DiveID",
                "Dive Site Name","Collecting Platform Name","Camera Type/Code",
                "Dive Start Date","Dive End Date","Dive Start Time",
                "Dive End Time","Dive Duration","Dive On Bottom Timestamp",
                "Dive Off Bottom Timestamp", "Max Depth (m)",
                "Minimum Depth (m)","North Latitude","South Latitude",
                "East Longitude", "West Longitude", "Project/Cruise Abstract",
                "Dive Abstract", "Dive Objectives", "Dive Keywords",
                "Underwater Cultural Heritage (UCH) Restrictions?"])
        # Write the data from the text fields
        writer.writerow([field1_data, field2_data, field3_data, field4_data,
            field5_data, field6_data, field7_data, field8_data, field9_data,
            field10_data, field11_data, field12_data, field13_data, field14_data,
            field15_data, field16_data, field17_data, field18_data, field19_data,
            field20_data,field21_data, field22_data, field23_data])

    # pop up message box to let the user know that data were saved successfully
    messagebox.showinfo("Data Saved",
    "Data have been saved to the 'metadata' spreadsheet in your working directory.")

    # Clear the data after submission
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)
    entry5.delete(0, tk.END)
    entry6.delete(0, tk.END)
    entry7.delete(0, tk.END)
    entry8.delete(0, tk.END)
    entry9.delete(0, tk.END)
    entry10.delete(0, tk.END)
    entry11.delete(0, tk.END)
    entry12.delete(0, tk.END)
    entry13.delete(0, tk.END)
    entry14.delete(0, tk.END)
    entry15.delete(0, tk.END)
    entry16.delete(0, tk.END)
    entry17.delete(0, tk.END)
    entry18.delete(0, tk.END)
    entry19.delete(0, tk.END)
    entry20.delete(0, tk.END)
    entry21.delete(0, tk.END)
    entry22.delete(0, tk.END)
    entry23.delete(0, tk.END)

def video_upload():
    """
    Retrieves and displays statistics about the selected video file
    when the upload button is clicked.

    This function extracts information about the video file specified
    by the user, including its duration, file size, and size per
    minute. It then calculates the ideal chunk size to ensure that
    video chunks are smaller than 5 GB. This information is displayed
    in a text box for the user to review.

    The function performs the following steps:
    1. Retrieves the filename of the video from a user interface
       element.
    2. Calculates the video's duration and file size.
    3. Computes the size of the video per minute of duration.
    4. Determines the ideal chunk size to ensure chunks are less
       than 5 GB.
    5. Updates a text box with the computed video statistics and
       recommendations.

    Returns:
    None

    Side Effects:
    - Updates the `video_information_box` with details about the video file, including:
      - Filename
      - Length of the video in minutes
      - Size of the video in gigabytes (GB)
      - Size per minute of video
      - Recommended chunk size to achieve chunks smaller than 5 GB

    Notes:
    - The `videoFileNameEntry` is expected to be an entry widget where the user 
      provides the path to the video file.
    - The `video_information_box` is expected to be a text widget where the video 
      statistics are displayed.
    - The `VideoFileClip` class from the `moviepy` library is used to get the video 
      duration.

    """

    try:
        desired_video_size = videoSizeEntry.get()
        if len(desired_video_size)<1:
            desired_video_size = 5
        else:
            desired_video_size = int(desired_video_size)
    except:
        messagebox.showinfo("Invalid Input",
            "Please enter an integer value for desired video size(GB). "+
            "Currently using the default value of 5 GB.")
        desired_video_size = 5

    video_file_path_string = videoFileNameEntry.get()
    video_file_path_list = [item.strip() for item in video_file_path_string.split(',')]

    for video_file_path in video_file_path_list:
        #clean_video_file_path = video_file_path.replace('"','')
        #video_file_path_list.replace(video_file_path, clean_video_file_path)
        file_exists = os.path.isfile(str(video_file_path))
        if not file_exists:
            messagebox.showerror("File not found",
                "This file ("+str(video_file_path)+") does not exist. Re-enter a file path")
            return None
    show_info_non_blocking("Number of Videos Selected: " +str(len(selected_files))+
            "\nFile List: " + str(selected_files))

def calculate_ideal_chunk(input_file, desired_chunk_size, progress_callback):
    chunk_dict = {}
    # Calculate the average bitrate of the video in bits per second
    #file_size = get_file_size(input_file)
    file_stats = os.stat(input_file)

    progress_callback(.05)

    file_size = file_stats.st_size

    progress_callback(.15)

    duration = get_video_duration(input_file)

    progress_callback(.25)
    average_bitrate = (file_size * 8) / duration
    print(f"Average bitrate of the video: {average_bitrate / (1024 ** 2):.2f} Mbps")
    desired_size_bytes = desired_chunk_size * 1024 * 1024
    desired_size_bits = desired_size_bytes * 8

    progress_callback(.30)
    # Convert bitrate from Mbps to bits per second
    # Calculate the length of the segment in seconds
    segment_length_seconds = desired_size_bits / average_bitrate

    progress_callback(.40)

    total_frame_count = get_video_frame_count(input_file)
    print("Total number of frames: ", total_frame_count)
    progress_callback(.65)
    total_chunks = int(duration // segment_length_seconds) + (1 if duration % segment_length_seconds > 0 else 0)
    print(f"Total number of chunks: {total_chunks}")
    progress_callback(.85)
    chunk_size_frames = int(total_frame_count // total_chunks) if total_chunks > 0 else 0
    print("Chunk size in frames: ", chunk_size_frames)
    progress_callback(.95)
    chunk_dict = {"chunk_frames":chunk_size_frames,"total_chunks":total_chunks, "total_frames":total_frame_count}
    progress_callback(0)

    #show_info_non_blocking("Chunk analysis complete. Beginning video chunking process...")

    return chunk_dict

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

def get_video_duration(input_file):
    # Run ffprobe to get the video duration
    command = [
        ffprobe_path, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1', input_file
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        # Extract the duration from the output string, splitting by '='
        duration = result.stdout.strip().split('=')[1]  # Get the value after '='
        return float(duration)  # Convert to float (duration is in seconds)
    else:
        raise Exception(f"Error in ffprobe: {result.stderr}")

def time_to_seconds(time_str):
    # Split the string by ':'
    hours, minutes, seconds = map(int, time_str.split(":"))
    
    # Convert to seconds and return
    return hours * 3600 + minutes * 60 + seconds

def split_video(filename, segment_length, file_name_dict, progress_callback):
    """
    Splits a video file into segments of a specified length and optionally converts them to a
    different format.

    This function takes a video file and divides it into multiple segments based on the provided
    segment length. The segments are saved with filenames that include the start and end times of
    each segment. The function supports different output formats based on the dropdown option. It
    also calls a progress callback function to report the progress of the segmentation.

    Parameters:
    filename (str): The path to the input video file that needs to be split.
    segment_length (int): The length of each video segment in seconds.
    progress_callback (function): A callback function that takes a single argument (float) 
    representing the progress as a percentage (0.0 to 1.0). 

    This function is called to update the progress of the segmentation process.

    Returns:
    None

    Raises:
    ValueError: If `segment_length` is not a positive integer.
    subprocess.CalledProcessError: If the ffmpeg command fails during execution.

    Notes:
    - The function reads the segment length, filename, and dropdown option for output format.
    - It uses the `VideoFileClip` class from the `moviepy` library to get the duration of the video.
    - The function constructs output filenames that include the start and end times of each segment.
    - The `ffmpeg` command-line tool is used for video processing. The exact command depends on the
      selected output format (e.g., no conversion, MP4, MOV).
    - Progress is updated by calling the `progress_callback` function with the fraction of completed 
      segments.
    - The `ffmpeg_path` variable must be defined and point to the ffmpeg executable for the command 
      to run correctly. This uses a relative path and should just work out of the box as-is.
    """
    
    file_path_list = list(file_name_dict.keys())
    first_result = file_path_list[0]
    #my_keyframes = get_keyframe_locations(filename)
    if filename == first_result:
        show_info_non_blocking("Video splitting operation started. Do not click the split video button again."+
            " Progress bar will update shortly...")
    
    video_file_path_string = videoFileNameEntry.get()
    video_file_path_list = [item.strip() for item in video_file_path_string.split(',')]

    for video_file_path in video_file_path_list:
        file_exists = os.path.isfile(str(video_file_path))
        if not file_exists:
            messagebox.showerror("File not found",
                "This file ("+str(video_file_path)+") does not exist. Re-enter a file path")
            return None

    try:
        desired_video_size = videoSizeEntry.get()
        if len(desired_video_size)<1:
            messagebox.showerror("Invalid Input",
                "Please enter an integer value for estimated video size(GB).")
            return None
        else:
            desired_video_size = int(desired_video_size)
    except:
        messagebox.showerror("Invalid Input",
            "Please enter an integer value for estimated video size(GB).")
        return None

    updated_file_name = file_name_dict.get(filename)
    dropdown_option = option_var.get()
    basename = os.path.basename(filename).split('.')[0]
    if dropdown_option == "No Conversion":
        extension = os.path.basename(filename).split('.')[1]
    else:
        extension = "." + dropdown_option.lower()
    #total_segments = int(duration / segment_length) + 1

    if updated_file_name is not None:
        basename = updated_file_name

    if len(basename)<6:
        messagebox.showerror("File Naming Convention",
            "The file name specified does not match the Descriptor_YYYMMDD naming convention. Re-enter a file path.")
        return None
    
    basename_date_check = basename[-8:]
    if basename_date_check.isdigit() == False:
        messagebox.showerror("Bad File Name Format",
            "Your file name should end with a date in this format: FILENAME_YYYYMMDD. Please enter a new file name in the appropriate section.")
        return None

    target_size_bytes = desired_video_size * 1073741824
    #print("BASENAME READ IN AS: " + basename)


    chunk_information = calculate_ideal_chunk(filename, desired_video_size,progress_callback)
    print(str(chunk_information))
    chunk_size_frames = chunk_information.get("chunk_frames")
    total_chunks = chunk_information.get("total_chunks")
    if len(str(segment_length))>=1:
        segment_length = int(segment_length)
        print("Segment length read as: " + str(segment_length))
        end_time = segment_length
    duration = get_video_duration(filename)
    print("Filename read as: " + str(filename))
    print("Duration read as: " + str(duration))
    start_time = 0
    i = 0

    frames_processed = chunk_size_frames * i
    total_frames = chunk_information.get("total_frames")
    remaining_frames = total_frames
    while frames_processed < total_frames:
    #while start_time < duration:
        print("START TIME LISTED AS: " + str(start_time))
        print("DURATION LISTED AS: " + str(duration))
        print("FRAME TRACKER: " +str(frames_processed)+" / " + str(total_frames))

        if remaining_frames < chunk_size_frames:
            chunk_size_frames = remaining_frames
        #print("END TIME LISTED AS: " + str(end_time))

        custom_dive_start_time = dive_start_entry.get()
        if len(str(custom_dive_start_time))>1:
            converted_custom_dive_start_time = time_to_seconds(str(custom_dive_start_time))
            real_time = start_time + converted_custom_dive_start_time
            start_time_converted = str(datetime.timedelta(seconds = round(real_time)))
            start_time_converted = start_time_converted.replace(":","")
        else:
            start_time_converted = str(datetime.timedelta(seconds = round(start_time)))
            start_time_converted = start_time_converted.replace(":","")
        if len(str(segment_length))>=1:
            end_time_converted = str(datetime.timedelta(seconds = end_time))
            end_time_converted = end_time_converted.replace(":","")
        #output = os.path.join(f"{basename}_part{i}."+str(extension))

        updated_output_directory = output_directory_entry.get()
        
        if len(str(updated_output_directory)) > 0:
            basename = os.path.join(updated_output_directory, basename)
            print("basename updated to: " +str(basename))

        output = os.path.join(f"{basename}T{start_time_converted}Z."+
            str(extension))
        print("Output listed as: " + str(output))

        if dropdown_option == "No Conversion":

            command = [
                ffmpeg_path,
                '-i', filename,  # Input file
                '-ss', str(start_time),  # Start time for the chunk in seconds
                '-c:v', 'copy',    # Copy video codec (no re-encoding)
                '-c:a', 'copy',    # Copy audio codec (no re-encoding)
                '-frames:v', str(chunk_size_frames),  # Number of frames for the chunk
                '-y',  # Overwrite output file if it exists
                #'-loglevel', 'debug',  # Increase verbosity
                #output  # Output file
            ]

            #command = [
            #    ffmpeg_path,
            #    '-i', filename,
            #    '-ss', str(start_time),
            #    '-to', str(min(end_time, duration)),
            #    '-c', 'copy',
            #    output
            #]

        elif dropdown_option == "MP4":
            output = output.replace('..','.')
            vcodec ='libx264'
            acodec = 'aac'
            command = [
                ffmpeg_path,
                '-ss', str(start_time),
                '-i', filename,
                #'-to', str(min(end_time, duration)),
                #"-fs", str(target_size_bytes),
                '-c:v', vcodec,
                '-c:a', acodec,
                '-frames:v', str(chunk_size_frames),  # Number of frames for the chunk
                '-strict', 'experimental',
            ]

        elif dropdown_option == "MOV":
            output = output.replace('..','.')
            vcodec ='libx264'
            acodec = 'aac'
            command = [
                ffmpeg_path,
                '-ss', str(start_time),
                '-i', filename,
                #'-to', str(min(end_time, duration)),
                #"-fs", str(target_size_bytes),
                '-c:v', vcodec,
                '-c:a', acodec,
                '-frames:v', str(chunk_size_frames),  # Number of frames for the chunk
                '-strict', 'experimental',
            ]
        # If end_time is provided, add the -to option to the command
        if len(str(segment_length))>=1:
            if start_time <1:
                command.extend(['-to', str(segment_length)])  # Optional end time for the chunk
            else:
                command.extend(['-to', str(end_time)])  # Optional end time for the chunk

        # Add the output file at the end
        command.append(output)

        # Run the ffmpeg command
        subprocess.run(command, check=True)
        chunk_duration = get_video_duration(output)
        start_time += chunk_duration
        if len(str(segment_length))>=1:
            end_time = start_time + segment_length

        #end_time += segment_length
        i += 1

        # Update progress
        
        frames_processed += chunk_size_frames
        remaining_frames -= chunk_size_frames
        progress = frames_processed/total_frames
        progress_callback(progress)
        if frames_processed >= total_frames:
            progress_callback(0)
            show_info_non_blocking("Your video has been successfully processed.")
            break

def show_info_non_blocking(message):
    # This function will display the error in a non-blocking manner using a new thread
    def show_message():
        messagebox.showinfo("Information", message)

    # Create a new thread to show the messagebox
    threading.Thread(target=show_message).start()

def get_keyframe_locations(input_file):
    # Run ffprobe to get keyframe timestamps
    command = [
        ffprobe_path, '-v', 'error', '-select_streams', 'v:0', 
        '-show_frames', '-show_entries', 'frame=pkt_pts_time,key_frame', 
        '-of', 'csv=p=0', input_file
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        keyframe_locations = []
        # Process the output to get keyframe timestamps
        for line in result.stdout.strip().splitlines():
            fields = line.split(',')
            timestamp = float(fields[0])  # Timestamp of the frame
            is_keyframe = int(fields[1])  # 1 if keyframe, 0 if not
            if is_keyframe == 1:
                keyframe_locations.append(timestamp)
        return keyframe_locations
    else:
        raise Exception(f"Error in ffprobe: {result.stderr}")

def update_progress(progress):
    """
    Updates progress bar based on number of chunks completed/remaining.
    """
    progress_bar['value'] = progress * 100
    page2.update_idletasks()

def get_file_size(file_name):
    """
    Retrieves the size of a file in gigabytes.

    This function calculates the size of the specified file and returns it in gigabytes. It uses the
    `os.stat` function to obtain file statistics and then converts the file size from bytes to
    gigabytes.

    Parameters:
    file_name (str): The path to the file whose size is to be determined.

    Returns:
    float: The size of the file in gigabytes.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    OSError: If there is an error accessing the file's statistics.

    Notes:
    - The file size is computed by dividing the size in bytes by `(1024 * 1024 * 1024)`,
      which converts bytes to gigabytes.
    - Ensure that the file path provided is correct and accessible to avoid potential errors.
    """
    # Gets the file size of the file name
    file_stats = os.stat(file_name)
    file_size = file_stats.st_size / (1024 * 1024 * 1024)
    return file_size

def create_page_content(my_page):
    """
    This function creates and configures the content for a specific page of the application,
    including a top frame with labels and a separator. The content includes instructions and
    descriptions for the user regarding the video chunking application. The labels are
    configured to wrap text appropriately based on their width.

    Parameters:
    my_page (tk.Frame): The Tkinter frame or page widget where the content will be added.
    This widget serves as the container for the various UI elements.

    Returns:
    None

    Side Effects:
    - Creates and packs a top frame containing labels with instructions and descriptions.
    - Adds a horizontal separator to visually separate the content.
    - Configures text wrapping for the description labels based on their width.

    Notes:
    - The `top_frame` is packed with padding and fills horizontally (`tk.X`).
    - `top_label` provides the title of the application with a bold font.
    - `top_description3` and `top_description4` provide instructions and descriptions with wrapping
      configured to adjust based on the widget's width.
    - The `separator` visually separates the top content from the rest of the page.
    """

    # Top frame
    top_frame = tk.Frame(my_page)
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    # Top label
    top_label = tk.Label(top_frame, text="OER Video Chunking Application", font=('Arial',
        16, 'bold'))
    top_label.pack(fill=tk.X)

    # Top description 3
    #top_description3 = tk.Label(top_frame, text="This application will split large video"+
    #    "files into chunks based on user input and generate a metadata file. Here are "+
    #    "the basic directions.",
    #    justify=tk.CENTER, font=('Arial', 10, 'bold'))
    #top_description3.bind('<Configure>',
    #    lambda e: top_description3.config(wraplength=top_description3.winfo_width()))
    #top_description3.pack(pady=5, fill=tk.X, expand=True)

    # Top description 4
    #top_description4 = tk.Label(top_frame, text="1. Enter the path to your video files (separated "+
        #"by commas), or use the browse function to select any number of local files. Click "+
        #"submit video to begin the process. \n2. Decide how to split the videos based on entered "+
        #"parameters. \n3. Enter any corresponding metadata for your video and generate a metadata "+
        #"spreadsheet.",
        #justify=tk.LEFT, font=('Arial', 10))
    #top_description4.bind('<Configure>',
    #    lambda e: top_description4.config(wraplength=top_description4.winfo_width()))
    #top_description4.pack(pady=5, fill=tk.X, expand=True)

    # Separator (Bar)
    separator = ttk.Separator(my_page, orient='horizontal')
    separator.pack(fill=tk.X, padx=10, pady=10)

def on_close():
    print("Closing application")
    app.quit()  # Exits the main loop and closes the application

def select_files():
    global selected_files
    selected_files = []
    # Create a Tkinter root window (hidden)

    # Open the file dialog to select files
    file_paths = filedialog.askopenfilenames(title="Select Files")

    # Print or process the selected files
    if file_paths:
        file_string = ""
        for file in file_paths:
            print(file)
            selected_files.append(file)
            file_string += str(file) + ','  # Build the string with files

# Insert the concatenated string into the Entry widget
        videoFileNameEntry.delete(0, tk.END)  # Clear any existing text
        videoFileNameEntry.insert(0, file_string.strip(','))
    else:
        print("No files selected.")

def select_directory():
    global selected_directory
    selected_directory = ""
    # Open the file dialog to select a directory
    directory_path = filedialog.askdirectory(title="Select Output Directory")

    # Check if a directory was selected
    if directory_path:
        print(f"Selected directory: {directory_path}")
        selected_directory = directory_path  # Store the directory path
        output_directory_entry.delete(0, tk.END)  # Clear any existing text
        output_directory_entry.insert(0, selected_directory.strip())
    else:
        print("No directory selected")

if __name__ == "__main__":

    # Initialize the main application window
    app = tk.Tk()
    app.title("OER Video Chunker")
    app.protocol("WM_DELETE_WINDOW", on_close)

    # Center the window on the screen
    app.update_idletasks()  # Ensure correct dimensions are calculated
    window_width = app.winfo_reqwidth()
    window_height = app.winfo_reqheight()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    app.geometry(f'+{x_position}+{y_position}')

    # Make sure the window pops up in front of other windows
    app.attributes('-topmost', True)
    app.after(1, lambda: app.attributes('-topmost', False))

    # Configure the main window to expand the widgets
    app.columnconfigure(0, weight=1)

    # Create a notebook (for tabbed pages)
    notebook = ttk.Notebook(app)
    notebook.pack(fill=tk.BOTH, expand=True)

    # First page (tab)
    page1 = ttk.Frame(notebook)
    notebook.add(page1, text="Select Files")

    # Second page (tab)
    page2 = ttk.Frame(notebook)
    notebook.add(page2, text="Split Files")

    # Third page (tab)
    page3 = ttk.Frame(notebook)
    notebook.add(page3, text="Generate Metadata")

    pageList = [page1,page2,page3]

    app.geometry("600x700")

    for page in pageList:
        create_page_content(page)

    ############################# PAGE 1 CONTENT STARTS HERE #################################
    bottom_frame = tk.Frame(page1)
    bottom_frame.pack(fill=tk.X, padx=10, pady=10)

    # Create a frame for the label of the required dimension at the required place
    label_frame = tk.Frame(bottom_frame, width = 200, height = 20)
    label_frame.pack(fill=tk.X,padx=5,pady=5)
    #label_frame.place(x = 60, y = 100)

    # Create the label and pack it to fill the whole frame (default anchor is Centre)
    test_label = tk.Label(label_frame, text = 'Enter Video Input and Output', font=('Arial', 12, 'bold'))
    test_label.pack(expand = True)

    videoFileName = tk.Label(label_frame, text="Select Input File(s):",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    videoFileName.pack(pady=5, fill=tk.X, expand=True)
    videoFileNameInstructions = tk.Label(label_frame,
        text="Use the browse button to select files or enter the filepath manually. Be sure to "+
        "include the extension (.mov or .mp4). Select multiple files with browse function with "+
        "the ctrl key.",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    videoFileNameInstructions.bind('<Configure>',
        lambda e: videoFileNameInstructions.config(wraplength=videoFileNameInstructions.winfo_width()))
    videoFileNameInstructions.pack(pady=5, fill=tk.X, expand=True)
    videoFileNameEntry = tk.Entry(label_frame)
    videoFileNameEntry.pack(pady=5, fill=tk.X, expand=True)

    # Create a browse button
    browse_button = tk.Button(label_frame, text="Browse Files",
        command=select_files, bg="lightGrey", fg="black")
    browse_button.pack(pady=20)

    updatedFileName = tk.Label(label_frame, text="Updated Video Name (if applicable): ",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    updatedFileName.pack(pady=5, fill=tk.X, expand=True)
    updatedFileNameInstructions = tk.Label(label_frame, text="If your file name does not"+
        " include the start date, enter a new filename that follows this convention: "+
        " FILENAME_YYYYMMDD (Example: Dive0982_20240916). For multiple files, separate with commas.",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    updatedFileNameInstructions.bind('<Configure>',
        lambda e: updatedFileNameInstructions.config(wraplength=updatedFileNameInstructions.winfo_width()))
    updatedFileNameInstructions.pack(pady=5, fill=tk.X, expand=True)
    updated_file_name_entry = tk.Entry(label_frame)
    updated_file_name_entry.pack(pady=5, fill=tk.X, expand=True)

    output_directory = tk.Label(label_frame, text="Output Directory Path (if applicable): ",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    output_directory.pack(pady=5, fill=tk.X, expand=True)

    output_directory_instructions = tk.Label(label_frame, text="Use the browse directory"+
        " button to select an output directory for your video chunks. If none is selected"+
        " your current working directory will be used.",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    output_directory_instructions.bind('<Configure>',
        lambda e: output_directory_instructions.config(wraplength=output_directory_instructions.winfo_width()))
    output_directory_instructions.pack(pady=5, fill=tk.X, expand=True)
    output_directory_entry = tk.Entry(label_frame)
    output_directory_entry.pack(pady=5, fill=tk.X, expand=True)

        # Create a browse button
    output_directory_button = tk.Button(label_frame, text="Browse Directories",
        command=select_directory, bg="lightGrey", fg="black")
    output_directory_button.pack(pady=20)

    #video_information_box = tk.Text(bottom_frame,height=6)
    #video_information_box.pack(pady=5,fill=tk.X, expand =True)
    #video_information_box.delete('1.0',END)
    #video_information_box.insert('1.0',
    #    "Video information and processing suggestions will be displayed here after clicking the "+
    #    "upload button below.")

    # Create a submit button
    #submit_button = tk.Button(bottom_frame, text="Upload Video",
    #    command=video_upload, bg="lightGrey", fg="black")
    #submit_button.pack(pady=20)

 ################### PAGE 2 CONTENT STARTS HERE ###################

    page2_bottom_frame = tk.Frame(page2)
    page2_bottom_frame.pack(fill=tk.X, padx=10, pady=10)

    # Create a frame for the label of the required dimension at the required place
    page2_label_frame = tk.Frame(page2_bottom_frame, width = 200, height = 20)
    page2_label_frame.pack(fill=tk.X,padx=5,pady=5)
    #label_frame.place(x = 60, y = 100)

    # Create the label and pack it to fill the whole frame (default anchor is Centre)
    page2_test_label = tk.Label(page2_label_frame, text = 'Enter Chunking Parameters',
        font=('Arial', 12, 'bold'))
    page2_test_label.pack(expand = True)

    videoSizeLabel = tk.Label(page2_label_frame, text="Desired Video Segment Size (GB):",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    videoSizeLabel.pack(pady=5, fill=tk.X, expand=True)
    videoSizeInstructions = tk.Label(page2_label_frame,
        text="Enter the maximum video segment size in GB",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    videoSizeInstructions.bind('<Configure>',
        lambda e: videoSizeInstructions.config(wraplength=videoSizeInstructions.winfo_width()))
    videoSizeInstructions.pack(pady=5, fill=tk.X, expand=True)
    videoSizeEntry = tk.Entry(page2_label_frame)
    videoSizeEntry.pack(pady=5, fill=tk.X, expand=True)

    chunkLength = tk.Label(page2_label_frame, text="Desired length of video chunks (in seconds): ",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    chunkLength.pack(pady=5, fill=tk.X, expand=True)
    chunkLengthInstructions = tk.Label(page2_label_frame,
        text="Enter the length (in seconds) that you would like each video chunk to be. Note that"+
        " the last chunk may be shorter than the rest.",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    chunkLengthInstructions.bind('<Configure>',
        lambda e: chunkLengthInstructions.config(wraplength=chunkLengthInstructions.winfo_width()))
    chunkLengthInstructions.pack(pady=5, fill=tk.X, expand=True)
    chunkLengthEntry = tk.Entry(page2_label_frame)
    chunkLengthEntry.pack(pady=5, fill=tk.X, expand=True)



    dive_start = tk.Label(page2_label_frame, text="Enter custom dive start time (HH:MM:SS): ",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    dive_start.pack(pady=5, fill=tk.X, expand=True)
    dive_start_instructions = tk.Label(page2_label_frame,
        text="Enter the start time of the video here. Ensure that you adhere to this format: HH:MM:SS",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    dive_start_instructions.bind('<Configure>',
        lambda e: dive_start_instructions.config(wraplength=dive_start_instructions.winfo_width()))
    dive_start_instructions.pack(pady=5, fill=tk.X, expand=True)
    dive_start_entry = tk.Entry(page2_label_frame)
    dive_start_entry.pack(pady=5, fill=tk.X, expand=True)


    dropdownLabel = tk.Label(page2_label_frame,
        text="If you want to convert your output files, select a new file type:",
        font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    dropdownLabel.pack(pady=5, fill=tk.X, expand=True)
    # Set options for video conversion dropdown list
    options = ["No Conversion", "MP4", "MOV"]

    # Set variable to contain user choice from conversion dropdown
    option_var = tk.StringVar(page2)
    option_var.set(options[0])  # Set default value

    # Create the OptionMenu dropdown widget
    dropdown = tk.OptionMenu(page2, option_var, *options)
    dropdown.pack(pady=20)

    # get the user choice from dropdown menu
    option_var.trace("w", on_option_change)

    progress_bar = ttk.Progressbar(page2, orient="horizontal", length=300,
        mode="determinate")
    progress_bar.pack(padx=10, pady=10)

    split_video_button = tk.Button(page2, text="Split Video",
        command=video_operation, bg="lightGrey", fg="black")
    split_video_button.pack(pady=20)

    ############################### PAGE 3 STARTS HERE #############################

    # Create a frame that will contain the canvas and the scrollbar
    outer_frame = tk.Frame(page3)
    outer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Create a canvas inside the outer_frame
    canvas = tk.Canvas(outer_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    label_frame = tk.Frame(canvas)

    # Add the label_frame to the canvas
    window = canvas.create_window((0, 0), window=label_frame, anchor="nw")

    # Adjust the size of the label_frame to match the outer_frame's width
    def on_configure(event):
        """
        Adjusts the canvas scroll region and updates the width of a window
        item when the canvas is resized.

        This function is an event handler that is triggered when the canvas
        widget is reconfigured, such as when its size changes. It performs
        the following actions:

        1. Updates the scroll region of the canvas to encompass all its items.
           This ensures that the canvas scrolls correctly to display all its 
           contents.
        2. Adjusts the width of a specific item (presumably a window or frame)
           within the canvas to match the current width of the canvas.

        Parameters:
        event (Event): An event object containing information about the
        configuration change, such as the new size of the canvas.

        Returns:
        None

        Side Effects:
        - Modifies the scroll region of the canvas to ensure all items are
          visible and scrollable.
        - Changes the width of the specified item within the canvas to match
          the canvas's width.

        Notes:
        - The `canvas` variable is assumed to be a `tk.Canvas` widget.
        - The `window` variable is assumed to be an item within the canvas
          whose width needs to be adjusted.

        """
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window, width=canvas.winfo_width())

    label_frame.bind("<Configure>", on_configure)

    # Populate the label_frame with widgets
    test_label = tk.Label(label_frame, text='Enter Video Metadata',
        font=('Arial', 10, 'bold'))
    test_label.pack(expand=True)

    # Adjust the canvas size when the outer frame is resized
    outer_frame.bind('<Configure>',
        lambda event: canvas.itemconfig(window, width=event.width))

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Bind the mousewheel event to the canvas
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    label1 = tk.Label(label_frame, text="* Project ID (or CruiseID): *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label1.pack(pady=5, fill=tk.X, expand=True)
    projectIdInstructions = tk.Label(label_frame, text="(Use ID assigned"+
        " by cruise or NOAA Ocean Exploration.)\nExample: NF2202",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    projectIdInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry1 = tk.Entry(label_frame)
    entry1.pack(pady=5, fill=tk.X, expand=True)

    label2 = tk.Label(label_frame, text="* DiveID: *", font=('Arial', 9, 'bold'),
        justify=tk.LEFT, anchor="w")
    label2.pack(pady=5, fill=tk.X, expand=True)
    diveIdInstructions = tk.Label(label_frame, text="(Open character.)"+
        "\nExamples: D01, D001, GE01, AL4039",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveIdInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry2 = tk.Entry(label_frame)
    entry2.pack(pady=5, fill=tk.X, expand=True)

    label3 = tk.Label(label_frame, text="* Dive Site Name: *", 
        font=('Arial', 9, 'bold'), justify=tk.LEFT, anchor="w")
    label3.pack(pady=5, fill=tk.X, expand=True)
    diveSiteNameInstructions = tk.Label(label_frame, text="(Open Text.)"+
        "\nExample: Guayanilla Canyon",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveSiteNameInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry3 = tk.Entry(label_frame)
    entry3.pack(pady=5, fill=tk.X, expand=True)

    label4 = tk.Label(label_frame, text="* Collecting Platform Name: *",
        font=('Arial', 9, 'bold'), justify=tk.LEFT, anchor="w")
    label4.pack(pady=5, fill=tk.X, expand=True)
    platformInstructions = tk.Label(label_frame, text="(Open Text."+
        " Include platform type.)\nExample: Global Explorer ROV",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    platformInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry4 = tk.Entry(label_frame)
    entry4.pack(pady=5, fill=tk.X, expand=True)

    label5 = tk.Label(label_frame, text="* Camera Type/Code: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label5.pack(pady=5, fill=tk.X, expand=True)
    cameraTypeInstructions = tk.Label(label_frame, text="(3CHIP/1080p/"+
        " PORT/HD/Canon/GoPro/etc.)\nExample: Canon HD",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    cameraTypeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry5 = tk.Entry(label_frame)
    entry5.pack(pady=5, fill=tk.X, expand=True)

    label6 = tk.Label(label_frame, text="* Dive Start Date: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label6.pack(pady=5, fill=tk.X, expand=True)
    startDateInstructions = tk.Label(label_frame, text="(YYMMDD)"+
        "\nExample: 20240610",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    startDateInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry6 = tk.Entry(label_frame)
    entry6.pack(pady=5, fill=tk.X, expand=True)

    label7 = tk.Label(label_frame, text="* Dive End Date: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label7.pack(pady=5, fill=tk.X, expand=True)
    endDateInstructions = tk.Label(label_frame, text="(YYMMDD)"+
        "\nExample: 20240611",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    projectIdInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry7 = tk.Entry(label_frame)
    entry7.pack(pady=5, fill=tk.X, expand=True)

    label8 = tk.Label(label_frame, text="* Dive Start Time: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label8.pack(pady=5, fill=tk.X, expand=True)
    startTimeInstructions = tk.Label(label_frame, text="(HHMMSS)"+
        "\nExample: 121500",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    startTimeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry8 = tk.Entry(label_frame)
    entry8.pack(pady=5, fill=tk.X, expand=True)

    label9 = tk.Label(label_frame, text="Dive End Time:",
        justify=tk.LEFT, anchor="w")
    label9.pack(pady=5, fill=tk.X, expand=True)
    endTimeInstructions = tk.Label(label_frame, text="(HHMMSS)"+
        "\nExample: 204500",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    endTimeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry9 = tk.Entry(label_frame)
    entry9.pack(pady=5, fill=tk.X, expand=True)

    label10 = tk.Label(label_frame, text="Dive Duration:",
        justify=tk.LEFT, anchor="w")
    label10.pack(pady=5, fill=tk.X, expand=True)
    endTimeInstructions = tk.Label(label_frame, text="(HH:MM:SS)"+
        "\nExample: 08:30:00",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    endTimeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry10 = tk.Entry(label_frame)
    entry10.pack(pady=5, fill=tk.X, expand=True)

    label11 = tk.Label(label_frame, text="Dive on Bottom Timestamp:",
        justify=tk.LEFT, anchor="w")
    label11.pack(pady=5, fill=tk.X, expand=True)
    diveOnBottomInstructions = tk.Label(label_frame, text="(HHMMSS)"+
        "\nExample: 130400",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveOnBottomInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry11 = tk.Entry(label_frame)
    entry11.pack(pady=5, fill=tk.X, expand=True)

    label12 = tk.Label(label_frame, text="Dive Off Bottom Timestamp:",
        justify=tk.LEFT, anchor="w")
    label12.pack(pady=5, fill=tk.X, expand=True)
    diveOffBottomInstructions = tk.Label(label_frame, text="(HHMMSS)"+
        "\nExample: 195800",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveOffBottomInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry12 = tk.Entry(label_frame)
    entry12.pack(pady=5, fill=tk.X, expand=True)

    label13 = tk.Label(label_frame, text="* Max Depth (m): *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label13.pack(pady=5, fill=tk.X, expand=True)
    maxDepthInstructions = tk.Label(label_frame, text="(This should be a #.)"+
        "\nExample: 50",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    maxDepthInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry13 = tk.Entry(label_frame)
    entry13.pack(pady=5, fill=tk.X, expand=True)

    label14 = tk.Label(label_frame, text="Minimum Depth (m):",
        justify=tk.LEFT, anchor="w")
    label14.pack(pady=5, fill=tk.X, expand=True)
    minDepthInstructions = tk.Label(label_frame, text="This should be a #."+
        "\nExample: Unknown",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    minDepthInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry14 = tk.Entry(label_frame)
    entry14.pack(pady=5, fill=tk.X, expand=True)

    label15 = tk.Label(label_frame, text="* North Latitude: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label15.pack(pady=5, fill=tk.X, expand=True)
    northLatitudeInstructions = tk.Label(label_frame, text="(Decimal"+
        " Degrees.)\nExample: 17.7648",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    northLatitudeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry15 = tk.Entry(label_frame)
    entry15.pack(pady=5, fill=tk.X, expand=True)

    label16 = tk.Label(label_frame, text="* South Latitude: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label16.pack(pady=5, fill=tk.X, expand=True)
    southLatitudeInstructions = tk.Label(label_frame, text="(Decimal"+
        " Degrees.)\nExample: 17.7627",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    southLatitudeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry16 = tk.Entry(label_frame)
    entry16.pack(pady=5, fill=tk.X, expand=True)

    label17 = tk.Label(label_frame, text="* East Longitude: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label17.pack(pady=5, fill=tk.X, expand=True)
    eastLongitudeInstructions = tk.Label(label_frame, text="(Decimal"+
        " Degrees.)\nExample: -66.7518",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    eastLongitudeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry17 = tk.Entry(label_frame)
    entry17.pack(pady=5, fill=tk.X, expand=True)

    label18 = tk.Label(label_frame, text="* West Longitude: *",
        font=('Arial', 9, 'bold'), justify=tk.LEFT, anchor="w")
    label18.pack(pady=5, fill=tk.X, expand=True)
    westLongitudeInstructions = tk.Label(label_frame, text="(Decimal"+
        " Degrees.)\nExample: -66.7532",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    westLongitudeInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry18 = tk.Entry(label_frame)
    entry18.pack(pady=5, fill=tk.X, expand=True)

    label19 = tk.Label(label_frame, text="* Project/Cruise Abstract: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label19.pack(pady=5, fill=tk.X, expand=True)
    projectAbstractInstructions = tk.Label(label_frame, text="(Open Text)",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    projectAbstractInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry19 = tk.Entry(label_frame)
    entry19.pack(pady=5, fill=tk.X, expand=True)

    label20 = tk.Label(label_frame, text="* Dive Abstract: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label20.pack(pady=5, fill=tk.X, expand=True)
    diveAbstractInstructions = tk.Label(label_frame, text="(Open Text)",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveAbstractInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry20 = tk.Entry(label_frame)
    entry20.pack(pady=5, fill=tk.X, expand=True)

    label21 = tk.Label(label_frame, text="* Dive Objectives: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label21.pack(pady=5, fill=tk.X, expand=True)
    diveObjectivesInstructions = tk.Label(label_frame, text="(Open Text)",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveObjectivesInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry21 = tk.Entry(label_frame)
    entry21.pack(pady=5, fill=tk.X, expand=True)

    label22 = tk.Label(label_frame, text="* Dive Keywords: *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label22.pack(pady=5, fill=tk.X, expand=True)
    diveKeywordsInstructions = tk.Label(label_frame, text="(Text, Text,"+
        " Text)",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    diveKeywordsInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry22 = tk.Entry(label_frame)
    entry22.pack(pady=5, fill=tk.X, expand=True)

    label23 = tk.Label(label_frame,
        text="* Underwater Cultural Heritage (UCH) Restrictions? *",
        font=('Arial', 9, 'bold'),justify=tk.LEFT, anchor="w")
    label23.pack(pady=5, fill=tk.X, expand=True)
    restrictionsInstructions = tk.Label(label_frame, text="(Yes/No)",
        font=('Arial', 8), justify=tk.LEFT, anchor="w")
    restrictionsInstructions.pack(pady=5, fill=tk.X, expand=True)
    entry23 = tk.Entry(label_frame)
    entry23.pack(pady=5, fill=tk.X, expand=True)

    # Update the scrollregion after adding all the widgets
    label_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Create submit button and add it to page3
    submit_button = tk.Button(page3, text="Generate Metadata",
        command=submit_data, bg="lightGrey", fg="black")
    submit_button.pack(pady=20)

    # Generate GUI
    app.mainloop()
