""" 
Laboration 1
Module for using nmap from python
Requirements:
1. Possible to save the result of the scan to a file
2. Use input/file to decide which ip-adress to scan
3. Menu where user choose what to do

Optional:
4. Developers imagination to add more functions in the tool
"""
import os
import ipaddress
import pprint
import time
import nmap

from swejob_tools import misc_tools

# Global variables
# Check if running on windows, otherwise assume linux
WINDOWS = misc_tools.is_windows()
ip_addr_str = "127.0.0.1"
subnet_mask_str = "32"
scan_flag_str = ""
output_flag_str = ""
settings_saved = True
status_msg = "Ready"
scan_res = []

def is_valid_ip_address(ip_string):
    """ Return true if a valid ip adress is provided as an argument """    
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def set_ip_address():
    """ 
    Get IP address and mask from user
    Setting global variables to valid ip_string and mask
    """
    # Accessing the global variables
    global ip_addr_str
    global settings_saved
    global status_msg
    status_msg = "Getting an IP address and mask from user"
    print_status_msg()
    global subnet_mask_str

    valid_ip_addr = False
    # loop until valid adress is entered
    while not valid_ip_addr:
        user_ip_addr = input("\x1b[4;43HEnter IP-address[aaa.bbb.ccc.ddd][/0-32]]:")
        #check if entered adress minus any mask provided is valid
        valid_ip_addr = is_valid_ip_address(user_ip_addr.split("/")[0])
    ip_addr_str = user_ip_addr.split("/")[0]
    settings_saved = False

    #Check if any mask is provided
    if "/" in user_ip_addr:
        # check to see if anything came after "/"
        if len(user_ip_addr.split("/")[1]) > 0:
            # If that was a number between 0 and 32
            subnet_mask_str = user_ip_addr.split("/")[1]
            if not(subnet_mask_str.isdigit() and int(subnet_mask_str) in range(0,33)):
                status_msg = "Incorrect subnet. The default 32-bit mask will be used"
                subnet_mask_str = "32"
        else:
            status_msg= "No subnet value provided. The default 32-bit mask will be used"
            subnet_mask_str = "32"
    else:
        status_msg = "No mask divider('/') provided. The default 32-bit mask will be used"
    print_status_msg()
    time.sleep(2)

def scan_target(ip_address,subnet_mask, scan_flags,output_flags):
    """ Scan target save result in scan_res"""
    global status_msg
    global scan_res
    # Add the path to nmap.exe if running on windows.
    # THIS PATH MIGHT NEED TO BE ALTERED FOR YOUR SYSTEM
    if WINDOWS:
        scan_obj = nmap.PortScanner(nmap_search_path = [r"C:\Program Files (x86)\Nmap\nmap.exe",])
    else:
        scan_obj = nmap.PortScanner()

    global scan_res
    host_str = ip_address  + "/" + subnet_mask
    # Update status message
    status_msg = f"Scanning {host_str}"
    print_status_msg()

    scan_obj.scan(host_str, arguments=scan_flag_str+output_flag_str)
    scan_res = scan_obj[ip_address]

    # Update status message
    status_msg = f"Scan of {host_str} is complete"
    print_status_msg()

def set_scan_flags():
    """
    User input which flags to select
    """
    global status_msg
    status_msg = "Running set_scan_flags"
    print_status_msg()

def set_output_flags():
    """ 
    User input which output flags to select
    """
    global status_msg
    status_msg = "Running set_output_flags"
    print_status_msg()

def scan_ip_address():
    """ 
    Call the scan_target function
    """
    scan_target(ip_addr_str, subnet_mask_str, scan_flag_str, output_flag_str)

def display_scan_result():
    """
    Print the result of the scan to the screen
    """
    global status_msg
    status_msg = "Printing the result from scan"
    print_status_msg()
    
    output_windows(scan_result)

def save_scan_result():
    """ 
    Save scan result to file
    """
    global status_msg
    status_msg = "Running save_scan_result"
    print_status_msg()

def load_scan_settings():
    """ 
    Load settings from file
    """
    global status_msg
    status_msg = "Running load_scan settings"
    print_status_msg()

def save_scan_settings():
    """
    Save settings from file
    """
    global status_msg
    status_msg = "Running save_scan settings"
    print_status_msg()

def display_help():
    """ 
    Print help to the screen
    """
    global status_msg
    status_msg = "Running display_help"
    print_status_msg()

def print_status_msg():
    """ 
    Print value of status_msg below menu
    """
    # print status_msg
    misc_tools.print_window([("Status: "+status_msg,)],1,42,75,True)
    time.sleep(1)

def output_window(output_text:list):
    misc_tools.print_window()
    
def settings_window():
    """ 
    Display thh setting swindow
    """
    # Make a string from the status of settings_saved
    save_string = "Settings are"
    if not settings_saved:
        save_string = save_string + " not"
    save_string = save_string + " saved"
    
    #create list for displaying settings
    setting_stats = [
        ("Current settings",),
        ("IP-address ".ljust(13),": ",ip_addr_str),
        ("Subnet mask ".ljust(13),": ",subnet_mask_str, " bits"),
        ("Scan flags ".ljust(13), ": ", scan_flag_str),
        ("Output flags ".ljust(13),": ",output_flag_str),
        ("",),
        (save_string,)
    ]
    # print the settings window in the upper left corner
    misc_tools.print_window(setting_stats,1,1,40,True)
    
# Constant with list of tuple containing:
# Selector, menu item and funcion to run
MAIN_MENU_LIST = [
        ("1", "Set IP address and mask", set_ip_address),
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

def main_menu():
    """ 
    Update status message, print menu and handle response
    """
    global status_msg
    status_msg = "Waiting for input. Select from main menu."
    print_status_msg()
    # print menu and wait for user selection
    misc_tools.menu(MAIN_MENU_LIST,5,32,10,1,menu_header="Nmap Tools by SweJob")

def main():
    """ 
    Main program
    """
    global status_msg

    while True:
        # Clear Screen
        os.system('cls')
        # Print the settings window upper left corner
        settings_window()        
        # Print any recieved status messages at the top, right of setting window
        print_status_msg()
        # Run main menu function
        main_menu()

if __name__ == "__main__":
    main()
