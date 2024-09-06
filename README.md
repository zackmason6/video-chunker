# video-chunker
Python Version 3.9
Code written by Zack Mason

This application is meant to break up videos into chunks for the OER video portal. It also generates metadata spreadsheets based on user input and allows for video renaming and file format conversions. 

Although it is currently functional, it is still a work in progress.

This application can be downloaded and run on its own but it is meant to be bundled as an executable and run that way. Currently it relies on an installation of FFMPEG. Because it is meant to be run as an exe, the path to the FFMPEG.exe file is relative and hardcoded. You may need to download FFMPEG and/or adjust the path within the code before running this application.

Here is a Google Drive link to the latest version of the executable: https://drive.google.com/file/d/1bHZ58VdmJ-XMGKxCcr9G6fk9GUNVcx4l/view?usp=drive_link

To Do:
1. Adjust naming conventions. OER video portal requires YYMMDD T HHMMSS Z.
1a. How will we get the year, month, and day? Should this be added to the metadata entry section? Should it be added to the first page? If so, we would likely need a scrollbar widget and the GUI would need to be reworked.
2. Should the user be able to select between splitting by size and splitting by time? Currently time is the only option but the user is expected to be able to calculate how large the file will be. They are given the size in GB per minute and can then likely do the math from there?
2a. If given the choice, I will likely need to move the size option from page one to page two. Maybe use a radio button selector with one entry field?
3. Need to really test the video converter tool. Have not tested on a wide variety of file types.
4. Clean up some ugly sections of code. Looking at you submit_data function. Yikes.
5. Process doesn't quit when GUI is closed. Is this a feature or a bug? You decide. Should likely ask if this is an issue or not. Might be kind of nice to close the window and let it run in the background.
6. Fix vertical resizing of GUI! Doesn't look great when resized vertically. Not super functional at the moment.
