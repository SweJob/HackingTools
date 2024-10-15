# HackingTools
### SweJob's small collection of home made utilities 
### as we are learning how to code for pentesting

HackingTools is a set of python scripts that are created as a part of my education as a pentester
The first tool created is: lab_1.py that was created as an attempt carry out the asignment "Laboration 1"
The instructions for us students for Laboration 1 was as follows:
---
### Laboration 1 - Kurs "Programmering för säkerhetstestare", ITST24 , IT-Högskolan
Module for using nmap from python
#### Requirements:
1. Possible to save the result of the scan to a file
2. Use input/file to decide which ip-adress to scan
3. Menu where user choose what to do
##### Optional:
4. Developers imagination to add more functions in the tool
---
## Features
- Make a list of IP addresses (with masks) to scan
save and restore the list to/from a file
- Make a list of arguments and ports
  save and restore the list to/from a file
- Scan the host according to the current settings
- Display the full scan result, a strippded down version
save and restore the full result to/from a file

Lab_1 is utilizing the misc_tools module that is found in swejob_tools
This provides for menus, keystroke handling, printing "windows" with text,
Additions to those methods are done in lab_1 to adhere to the specific requirements

Navigate according to the menu's and provided information in the status window that is located on top

NOTE:
As some of the displaying requires a certain height and width of the terminal, there are some checks made if the terminal window is to small.
The program will loop until you set the window to the minumum size

This text you see here is  written in Markdown! 
## Tech

HackingTools Lab_1 is using other external libraries:
- python-nmap 0.7.1 - https://pypi.org/project/python-nmap/ - for the actual scanning
- getkey - forked from https://github.com/spikeynick/getkey.git - to read keystrokes in win and linux
- colorama 0.4.6 - https://pypi.org/project/colorama/ - to play with colors on the screen
- pathvalidate 3.2.1 - https://pypi.org/project/pathvalidate/ - to work with files

## This text was made with dillinger.io
