import os
import sys
import pandas as pd
#import docx
import csv
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import END
import ffmpeg
import threading

########## THINGS TO ADD #############
# VIDEO CONVERSIONS?

# Path to the ffmpeg executable
ffmpeg_path = 'C:/Users/Zack_Mason/Desktop/coding/codingProjects/videoChunker/ffmpeg-2024-08-15-git-1f801dfdb5-essentials_build/bin/ffmpeg.exe'

# Update the path to ffmpeg in the ffmpeg-python library
ffmpeg._ffmpeg_exe = ffmpeg_path

def video_operation():
    videoFilePath = videoFileNameEntry.get()
    file_exists = os.path.isfile(videoFilePath)
    if not file_exists:
        messagebox.showinfo("File not found", "The file specified does not exist. Re-enter a file path")
    else:
        #messagebox.showinfo("File found", "This test is successful")
        segment_length = chunkLengthEntry.get()
        threading.Thread(target=split_video, args=(videoFilePath, segment_length, update_progress)).start()
        #split_video(videoFilePath, segment_length)
        messagebox.showinfo("Video Split","Video split operation started. Do not click the split video button again.\nProgress bar will update shortly...")

# Function to handle the submit button click
def submit_data():
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
    
    # File name for the CSV
    filename = 'metadata.csv'
    
    # Check if the file exists to determine whether to write headers
    file_exists = os.path.isfile(filename)
    
    # Open the CSV file for appending data
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers if the file is being created for the first time
        if not file_exists:
            writer.writerow(["Project ID (or CruiseID)", "DiveID", "Dive Site Name","Collecting Platform Name","Camera Type/Code","Dive Start Date","Dive End Date","Dive Start Time","Dive End Time","Dive Duration","Dive On Bottom Timestamp", "Dive Off Bottom Timestamp", "Max Depth (m)", "Minimum Depth (m)", "North Latitude", "South Latitude", "East Longitude", "West Longitude", "Project/Cruise Abstract","Dive Abstract", "Dive Objectives", "Dive Keywords", "Underwater Cultural Heritage (UCH) Restrictions?"])
        
        # Write the data from the text fields
        writer.writerow([field1_data, field2_data, field3_data, field4_data, field5_data, field6_data, field7_data, field8_data, field9_data, field10_data, field11_data, field12_data, field13_data, field14_data, field15_data, field16_data, field17_data, field18_data, field19_data, field20_data,field21_data, field22_data, field23_data])
    
    # Inform the user that the data has been saved
    messagebox.showinfo("Data Saved", "The data has been successfully saved to the 'metadata' spreadsheet in your working directory.")
    
    # Clear the entry fields after submission (optional)
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
    filename = videoFileNameEntry.get()
    clip = VideoFileClip(filename)
    duration = clip.duration
    durationMinutes = duration/60
    fileSize = getFileSize(filename)
    sizePerMinute = fileSize/durationMinutes
    idealChunkSize = (5/sizePerMinute) * 60

    video_information_box.delete('1.0',END)
    video_information_box.insert('1.0', "Filename read as: " + str(filename))
    video_information_box.insert('2.0', "\nLength of video (minutes): " + str(durationMinutes))
    video_information_box.insert('3.0', "\nSize of video (GB): " + str(fileSize) + " GB")
    video_information_box.insert('4.0', "\nSize per minute of video: " + str(sizePerMinute) + " GB")

    video_information_box.insert('5.0', "\n\nIn order to receive video chunks smaller than 5GB, specify that your chunks are less than " + str(idealChunkSize) + " seconds long.")

def split_video(filename, segment_length, progress_callback):
    segment_length = int(segment_length)
    clip = VideoFileClip(filename)
    duration = clip.duration
    print("Segment length read as: " + str(segment_length))
    print("Filename read as: " + str(filename))
    print("Duration read as: " + str(duration))

    start_time = 0
    end_time = segment_length
    i = 1
    
    basename = os.path.basename(filename).split('.')[0]
    extension = os.path.basename(filename).split('.')[1]
    total_segments = int(duration / segment_length) + 1

    while start_time < duration:
        output = os.path.join(f"{basename}_part{i}."+str(extension))
        print("Output listed as: " + str(output))
        
        # Construct ffmpeg command
        #command = [
        #    ffmpeg_path,
        #    '-ss', str(start_time),
        #    '-i', filename,
        #    '-to', str(min(end_time, duration)),
        #    '-c:v', 'libx264',  # Set video codec to H.264
        #    '-c:a', 'aac',      # Set audio codec to AAC
        #    '-strict', 'experimental',  # Allow experimental codecs if needed
        #    output
        #]

        # Construct ffmpeg command
        command = [
            ffmpeg_path,
            '-ss', str(start_time),
            '-i', filename,
            '-to', str(min(end_time, duration)),
            '-c', 'copy',
            output
        ]

        # Run the command
        subprocess.run(command, check=True)

        start_time = end_time
        end_time += segment_length
        i += 1
        
        # Update progress
        progress = i - 1
        progress_callback(progress / total_segments)

    print(f'Video split into {i-1} parts.')

def update_progress(progress):
    progress_bar['value'] = progress * 100
    page2.update_idletasks()

def getMetadataFile(listOfFiles):
    metadataFile = input("Which file contains your metadata? ")
    if metadataFile not in listOfFiles:
        print("Invalid entry.\n")
        getMetadataFile(listOfFiles)
    return metadataFile

def getFileSize(file_name):
    file_stats = os.stat(file_name)
    fileSize = file_stats.st_size / (1024 * 1024 * 1024)
    return fileSize

def getData(dataSheet,columnHeader):
  """
  This function performs all of the necessary data gathering from the tracking spreadsheet.
  Additionally, it passes this information to the sendMimeEmail function.
  """
  cellValue = dataSheet.loc[1, columnHeader]
  return cellValue

def create_page_content(page):
    # Top frame
    top_frame = tk.Frame(page)
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    # Top label
    top_label = tk.Label(top_frame, text="OER Video Chunking Application", font=('Arial', 16, 'bold'))
    top_label.pack(fill=tk.X)

    # Top description 3
    top_description3 = tk.Label(top_frame, text="This application will split large video files into chunks based on user input and generate a metadata file. Here are the basic directions.",
                                 justify=tk.CENTER, font=('Arial', 10, 'bold'))
    top_description3.bind('<Configure>', lambda e: top_description3.config(wraplength=top_description3.winfo_width()))
    top_description3.pack(pady=5, fill=tk.X, expand=True)

    # Top description 4
    top_description4 = tk.Label(top_frame, text="1. Enter the path to your video file and click submit video to get video information and processing suggestions. \n2. Decide how to split the video based on entered parameters. \n3. Enter any corresponding metadata for your video and generate a metadata spreadsheet.",
                                 justify=tk.LEFT, font=('Arial', 10))
    top_description4.bind('<Configure>', lambda e: top_description4.config(wraplength=top_description4.winfo_width()))
    top_description4.pack(pady=5, fill=tk.X, expand=True)

    # Separator (Bar)
    separator = ttk.Separator(page, orient='horizontal')
    separator.pack(fill=tk.X, padx=10, pady=10)

if __name__ == "__main__":

    # Initialize the main application window
    app = tk.Tk()
    app.title("OER Video Chunker")

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
    notebook.add(page1, text="Upload Video")

    # Second page (tab)
    page2 = ttk.Frame(notebook)
    notebook.add(page2, text="Split Video")

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
    test_label = tk.Label(label_frame, text = 'Enter Video Information', font=('Arial', 12, 'bold'))
    test_label.pack(expand = True)

    videoFileName = tk.Label(label_frame, text="Video File Path:", font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    videoFileName.pack(pady=5, fill=tk.X, expand=True)
    videoFileNameEntry = tk.Entry(label_frame)
    videoFileNameEntry.bind('<Configure>', lambda e: videoFileNameEntry.config(wraplength=videoFileNameEntry.winfo_width()))
    videoFileNameEntry.pack(pady=5, fill=tk.X, expand=True)
    videoFileNameInstructions = tk.Label(label_frame, text="If this video is in your working directory, just enter the filename. Be sure to include the extension (.mov or .mp4). Get the full file path by finding the file in file explorer, right clicking it and selecting 'properties.'", font=('Arial', 8), justify=tk.LEFT, anchor="w")
    videoFileNameInstructions.bind('<Configure>', lambda e: videoFileNameInstructions.config(wraplength=videoFileNameInstructions.winfo_width()))
    videoFileNameInstructions.pack(pady=5, fill=tk.X, expand=True)

    video_information_box = tk.Text(bottom_frame,height=10)
    video_information_box.bind('<Configure>', lambda e: video_information_box.config(wraplength=video_information_box.winfo_width()))
    video_information_box.pack(pady=5,fill=tk.X, expand =True)
    video_information_box.delete('1.0',END)
    video_information_box.insert('1.0', "Video information and processing suggestions will be displayed here after clicking the upload button below.")

    # Create a submit button
    submit_button = tk.Button(bottom_frame, text="Upload Video", command=video_upload, bg="lightGrey", fg="black")
    submit_button.pack(pady=20)

    ################################### PAGE 2 CONTENT STARTS HERE ############################################

    page2_bottom_frame = tk.Frame(page2)
    page2_bottom_frame.pack(fill=tk.X, padx=10, pady=10)

    # Create a frame for the label of the required dimension at the required place
    page2_label_frame = tk.Frame(page2_bottom_frame, width = 200, height = 20)
    page2_label_frame.pack(fill=tk.X,padx=5,pady=5)
    #label_frame.place(x = 60, y = 100)

    # Create the label and pack it to fill the whole frame (default anchor is Centre) 
    page2_test_label = tk.Label(page2_label_frame, text = 'Enter Chunking Parameters', font=('Arial', 12, 'bold'))
    page2_test_label.pack(expand = True)

    updatedFileName = tk.Label(page2_label_frame, text="Updated Video Name (if applicable): ", font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    updatedFileName.pack(pady=5, fill=tk.X, expand=True)
    updatedFileNameEntry = tk.Entry(page2_label_frame)
    updatedFileNameEntry.bind('<Configure>', lambda e: updatedFileNameEntry.config(wraplength=updatedFileNameEntry.winfo_width()))
    updatedFileNameEntry.pack(pady=5, fill=tk.X, expand=True)
    updatedFileNameInstructions = tk.Label(page2_label_frame, text="If you would like to change the name of the output files to something that doesn't match the input filename, enter that here. Otherwise, leave this blank.", font=('Arial', 8), justify=tk.LEFT, anchor="w")
    updatedFileNameInstructions.bind('<Configure>', lambda e: updatedFileNameInstructions.config(wraplength=updatedFileNameInstructions.winfo_width()))
    updatedFileNameInstructions.pack(pady=5, fill=tk.X, expand=True)

    chunkLength = tk.Label(page2_label_frame, text="Desired length of video chunks (in seconds): ", font=('Arial', 10, 'bold'), justify=tk.LEFT, anchor="w")
    chunkLength.pack(pady=5, fill=tk.X, expand=True)
    chunkLengthEntry = tk.Entry(page2_label_frame)
    chunkLengthEntry.bind('<Configure>', lambda e: chunkLengthEntry.config(wraplength=chunkLengthEntry.winfo_width()))
    chunkLengthEntry.pack(pady=5, fill=tk.X, expand=True)
    chunkLengthInstructions = tk.Label(page2_label_frame, text="Enter the length (in seconds) that you would like each video chunk to be. Note that the last chunk may be shorter than the rest.", font=('Arial', 8), justify=tk.LEFT, anchor="w")
    chunkLengthInstructions.bind('<Configure>', lambda e: chunkLengthInstructions.config(wraplength=chunkLengthInstructions.winfo_width()))
    chunkLengthInstructions.pack(pady=5, fill=tk.X, expand=True)

    progress_bar = ttk.Progressbar(page2, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(padx=10, pady=10)

    split_video_button = tk.Button(page2, text="Split Video", command=video_operation, bg="lightGrey", fg="black")
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
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window, width=canvas.winfo_width())

    label_frame.bind("<Configure>", on_configure)

    # Populate the label_frame with widgets
    test_label = tk.Label(label_frame, text='Enter Video Metadata', font=('Arial', 10, 'bold'))
    test_label.pack(expand=True)

    # Adjust the canvas size when the outer frame is resized
    outer_frame.bind('<Configure>', lambda event: canvas.itemconfig(window, width=event.width))

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Bind the mousewheel event to the canvas
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    label1 = tk.Label(label_frame, text="Project ID (or CruiseID):", justify=tk.LEFT, anchor="w")
    label1.pack(pady=5, fill=tk.X, expand=True)
    entry1 = tk.Entry(label_frame)
    entry1.pack(pady=5, fill=tk.X, expand=True)

    label2 = tk.Label(label_frame, text="DiveID:", justify=tk.LEFT, anchor="w")
    label2.pack(pady=5, fill=tk.X, expand=True)
    entry2 = tk.Entry(label_frame)
    entry2.pack(pady=5, fill=tk.X, expand=True)

    label3 = tk.Label(label_frame, text="Dive Site Name:", justify=tk.LEFT, anchor="w")
    label3.pack(pady=5, fill=tk.X, expand=True)
    entry3 = tk.Entry(label_frame)
    entry3.pack(pady=5, fill=tk.X, expand=True)

    label4 = tk.Label(label_frame, text="Collecting Platform Name:", justify=tk.LEFT, anchor="w")
    label4.pack(pady=5, fill=tk.X, expand=True)
    entry4 = tk.Entry(label_frame)
    entry4.pack(pady=5, fill=tk.X, expand=True)

    label5 = tk.Label(label_frame, text="Camera Type/Code:", justify=tk.LEFT, anchor="w")
    label5.pack(pady=5, fill=tk.X, expand=True)
    entry5 = tk.Entry(label_frame)
    entry5.pack(pady=5, fill=tk.X, expand=True)

    label6 = tk.Label(label_frame, text="Dive Start Date:", justify=tk.LEFT, anchor="w")
    label6.pack(pady=5, fill=tk.X, expand=True)
    entry6 = tk.Entry(label_frame)
    entry6.pack(pady=5, fill=tk.X, expand=True)

    label7 = tk.Label(label_frame, text="Dive End Date:", justify=tk.LEFT, anchor="w")
    label7.pack(pady=5, fill=tk.X, expand=True)
    entry7 = tk.Entry(label_frame)
    entry7.pack(pady=5, fill=tk.X, expand=True)

    label8 = tk.Label(label_frame, text="Dive Start Time:", justify=tk.LEFT, anchor="w")
    label8.pack(pady=5, fill=tk.X, expand=True)
    entry8 = tk.Entry(label_frame)
    entry8.pack(pady=5, fill=tk.X, expand=True)

    label9 = tk.Label(label_frame, text="Dive End Time:", justify=tk.LEFT, anchor="w")
    label9.pack(pady=5, fill=tk.X, expand=True)
    entry9 = tk.Entry(label_frame)
    entry9.pack(pady=5, fill=tk.X, expand=True)

    label10 = tk.Label(label_frame, text="Dive Duration:", justify=tk.LEFT, anchor="w")
    label10.pack(pady=5, fill=tk.X, expand=True)
    entry10 = tk.Entry(label_frame)
    entry10.pack(pady=5, fill=tk.X, expand=True)

    label11 = tk.Label(label_frame, text="Dive on Bottom Timestamp:", justify=tk.LEFT, anchor="w")
    label11.pack(pady=5, fill=tk.X, expand=True)
    entry11 = tk.Entry(label_frame)
    entry11.pack(pady=5, fill=tk.X, expand=True)

    label12 = tk.Label(label_frame, text="Dive Off Bottom Timestamp:", justify=tk.LEFT, anchor="w")
    label12.pack(pady=5, fill=tk.X, expand=True)
    entry12 = tk.Entry(label_frame)
    entry12.pack(pady=5, fill=tk.X, expand=True)

    label13 = tk.Label(label_frame, text="Max Depth (m):", justify=tk.LEFT, anchor="w")
    label13.pack(pady=5, fill=tk.X, expand=True)
    entry13 = tk.Entry(label_frame)
    entry13.pack(pady=5, fill=tk.X, expand=True)

    label14 = tk.Label(label_frame, text="Minimum Depth (m):", justify=tk.LEFT, anchor="w")
    label14.pack(pady=5, fill=tk.X, expand=True)
    entry14 = tk.Entry(label_frame)
    entry14.pack(pady=5, fill=tk.X, expand=True)

    label15 = tk.Label(label_frame, text="North Latitude:", justify=tk.LEFT, anchor="w")
    label15.pack(pady=5, fill=tk.X, expand=True)
    entry15 = tk.Entry(label_frame)
    entry15.pack(pady=5, fill=tk.X, expand=True)

    label16 = tk.Label(label_frame, text="South Latitude:", justify=tk.LEFT, anchor="w")
    label16.pack(pady=5, fill=tk.X, expand=True)
    entry16 = tk.Entry(label_frame)
    entry16.pack(pady=5, fill=tk.X, expand=True)

    label17 = tk.Label(label_frame, text="East Longitude:", justify=tk.LEFT, anchor="w")
    label17.pack(pady=5, fill=tk.X, expand=True)
    entry17 = tk.Entry(label_frame)
    entry17.pack(pady=5, fill=tk.X, expand=True)

    label18 = tk.Label(label_frame, text="West Longitude:", justify=tk.LEFT, anchor="w")
    label18.pack(pady=5, fill=tk.X, expand=True)
    entry18 = tk.Entry(label_frame)
    entry18.pack(pady=5, fill=tk.X, expand=True)

    label19 = tk.Label(label_frame, text="Project/Cruise Abstract:", justify=tk.LEFT, anchor="w")
    label19.pack(pady=5, fill=tk.X, expand=True)
    entry19 = tk.Entry(label_frame)
    entry19.pack(pady=5, fill=tk.X, expand=True)

    label20 = tk.Label(label_frame, text="Dive Abstract:", justify=tk.LEFT, anchor="w")
    label20.pack(pady=5, fill=tk.X, expand=True)
    entry20 = tk.Entry(label_frame)
    entry20.pack(pady=5, fill=tk.X, expand=True)
    
    label21 = tk.Label(label_frame, text="Dive Objectives:", justify=tk.LEFT, anchor="w")
    label21.pack(pady=5, fill=tk.X, expand=True)
    entry21 = tk.Entry(label_frame)
    entry21.pack(pady=5, fill=tk.X, expand=True)

    label22 = tk.Label(label_frame, text="Dive Keywords:", justify=tk.LEFT, anchor="w")
    label22.pack(pady=5, fill=tk.X, expand=True)
    entry22 = tk.Entry(label_frame)
    entry22.pack(pady=5, fill=tk.X, expand=True)

    label23 = tk.Label(label_frame, text="Underwater Cultural Heritage (UCH) Restrictions?", justify=tk.LEFT, anchor="w")
    label23.pack(pady=5, fill=tk.X, expand=True)
    entry23 = tk.Entry(label_frame)
    entry23.pack(pady=5, fill=tk.X, expand=True)

    # Update the scrollregion after adding all the widgets
    label_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Create submit button and add it to page3
    submit_button = tk.Button(page3, text="Generate Metadata", command=submit_data, bg="lightGrey", fg="black")
    submit_button.pack(pady=20)

    # Generate GUI
    app.mainloop()