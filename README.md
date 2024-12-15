# video-chunker
Python Version 3.9
Code written by Zack Mason

This application is meant to break up videos into chunks for the OER video portal. It also generates metadata spreadsheets based on user input and allows for video renaming and file format conversions. 

Although it is currently functional, it is still a work in progress.

This application can be downloaded and run on its own but it is meant to be bundled as an executable and run that way. Currently it relies on an installation of FFMPEG. Because it is meant to be run as an exe, the path to the FFMPEG.exe file is relative and hardcoded. You may need to download FFMPEG and/or adjust the path within the code before running this application.

Here is a Google Drive link to the latest (READ: incredibly out of date) version of the executable: https://drive.google.com/file/d/1bHZ58VdmJ-XMGKxCcr9G6fk9GUNVcx4l/view?usp=drive_link

To Do:
1. Adjust naming conventions. OER video portal requires YYMMDD T HHMMSS Z.
1a. Not sure this is actually still an issue. Will need to double check. If so, maybe use created date?
# 2. Interface says GB but behind the scenes everything is operating on MB for testing. This is a big one if you are using this application.
3. Clean up some ugly sections of code. Looking at you submit_data function. Yikes.
4. Fix vertical resizing of GUI! Doesn't look great when resized vertically. Not super functional at the moment.
# 5. Not encoding the output file will result in some dropped or duplicate frames. Not many, but some. This is because ffmpeg only cuts at key frames and sometimes they aren't where you expect them to be. I've tried to minimize the damage here and I think it's fine for a number of applications but there has to be a way to maintain the speed of the copy option and still allow the user a modicum of control over the chunk sizes. If you're worried about it, just re-encode the video as the same thing in the drop down menu. MP4 to MP4 or MOV to MOV. That should fix it but it will be slower.
5a. Could just cut everything at key frames and call it a day but splicing these cuts back together caused some issues and I ran out of time. Possibly a fix sometime down the line.
