# JHOVE-Digital-Specifications-lite-Automation
This repository is for bare-bones automation of writing digital specifications using JHOVE and an accompanying Python script. It's nothing fancy, but its simplicity allows the process to be versatile and easily integrated into more complex workflows by real programmers.

Gist to program 7.16.26: https://gist.github.com/Wadlesdh/a1eeae89eec4c84b4aea60720e049d2c

The only programs you need to use these instructions are JHOVE (and by extension Java) and Python.

1. Run JHOVE and input the following command:

    jhove -h xml -k "filelocation" -o "outputlocation\filename.xml"

2. Paste the below Python code into the terminal. Remember to enter the "input_location\filename.xml" and "output_location\filename.csv". You may have to launch Python with the "python" command.

3. You should see your (mostly) formatted digital specifications in the terminal, along with a non-formatted .csv file of the same data in our output location.

4. If needed, copy and paste the digital specifications into a word processor for future use.

5. Edit formatting as necessary and look for errors before populating metadata worksheets.

Changelog:

July 21, 2026: Edited terminal script to also show validity and error messages in a separate list. Added a GUI script (NOTE: only runs as intended on Windows; Mac-compatible version is in the works).
