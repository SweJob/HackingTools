import ipaddress
import nmap
from swejob_tools import misc_tools
import sys
import getopt

# Check if running on windows, otherwise assume linux
WINDOWS = misc_tools.is_windows()

# get a list of command line arguments
# no_of_arguments = len(sys.argv) # not implemented yet

# compare arguments with list of valid arguments
# not implemented yet

def set_ip_address():
    print("Running set_ip_address")
    
def set_scan_flags():
    print("Running set_scan_flags")

def set_output_flags():
    print("Running set_output_flags")
    
def scan_ip_address():
    print("Running scan_ip_address")
    
def display_scan_result():
    print("Running display_scan_result")

def save_scan_result():
    print("Running save_scan_result")

def load_scan_settings():
    print("Running load_scan settings")

def save_scan_settings():
    print("Running save_scan settings")

def display_help():
    

def main():
    main_menu_list = [
        ("1", "Set IP address", set_ip_address),
        ("2", "Set scan flags", set_scan_flags),
        ("3", "Set output flags", set_output_flags),
        ("4", "Scan IP address", scan_ip_address),
        ("5", "Display scan result", display_scan_result),
        ("6", "Save scan result to file", save_scan_result),
        ("7", "Load scan settings from file", load_scan_settings),
        ("8", "Save scan settings to file", save_scan_settings),
        ("9", "Help",display_help),
        ("0", "Quit program", misc_tools.stop_program)        
        
    ]

   