# video-chunker
Python Version 3.9
Code written by Zack Mason

This application is meant to segment video files specifically for the OER video portal. It also generates metadata spreadsheets based on user input and allows for video renaming, compression, and file format conversions. 

This application can be downloaded and run on its own but it is meant to be bundled as an executable and run that way. Currently it relies on an installation of FFmpeg and FFprobe. Because it is meant to be run as an exe, the path to the FFmpeg.exe and FFprobe.exe files are relative and hardcoded. You may need to download these files and/or adjust the path within the code before running this application.

Here is a Google Drive link to the latest (READ: incredibly out of date) version of the executable: https://drive.google.com/file/d/1bHZ58VdmJ-XMGKxCcr9G6fk9GUNVcx4l/view?usp=drive_link

To Do:
1. Adjust naming conventions. OER video portal requires YYMMDD T HHMMSS Z. Other groups have different naming conventions. Should convention adherence be dropped from the application?
2. Fix vertical resizing of GUI. Some visual inconsistencies there.
3. Need to test if the "no encoding" option is still dropping/garbling any frames. I've implemented a fix but need to do frame counts on output files.
