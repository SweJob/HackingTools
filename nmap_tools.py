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
# import pprint
import time
import nmap
from colorama import Fore
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

def set_status_msg(msg):
    """
    Set status_msg to msg or 'Ready' if msg is empty 
    """
    global status_msg
    if msg == "":
        status_msg = "Ready"
    else:
        status_msg = msg

def is_valid_ip_address(ip_string):
    """ 
    Return true if a valid ip adress is provided as an argument 
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def settings_changed(changed):
    """ 
    set global settings_saved to False
    """
    global settings_saved
    settings_saved = not changed

def set_ip_address():
    """ 
    Get IP address and mask from user
    Setting global variables to valid ip_string and mask
    """
    # Accessing the global variables
    global ip_addr_str
    global subnet_mask_str
    set_status_msg("Getting an IP address and mask from user")
    print_status_msg()
    valid_ip_addr = False
    # loop until valid adress is entered
    while not valid_ip_addr:
        # Clear previous entry
        misc_tools.pos_print(5,43," "*(misc_tools.get_terminal_width()-46))
        # Get input , prompt under status message
        user_ip_addr = input("\x1b[5;43HEnter IP-address[aaa.bbb.ccc.ddd][/0-32]]: ")
        #check if entered adress minus any mask provided is valid
        valid_ip_addr = is_valid_ip_address(user_ip_addr.split("/")[0])
    ip_addr_str = user_ip_addr.split("/")[0]
    # A setting was changed
    settings_changed(True)

    #Check if any mask is provided
    if "/" in user_ip_addr:
        # check to see if anything came after "/"
        if len(user_ip_addr.split("/")[1]) > 0:
            # If that was a number between 0 and 32
            subnet_mask_str = user_ip_addr.split("/")[1]
            if not(subnet_mask_str.isdigit() and int(subnet_mask_str) in range(0,33)):
                set_status_msg("Incorrect subnet. The default 32-bit mask will be used")
                subnet_mask_str = "32"
        else:
            set_status_msg("No subnet value provided. The default 32-bit mask will be used")
            subnet_mask_str = "32"
    else:
        set_status_msg("No mask divider('/') provided. The default 32-bit mask will be used")
    print_status_msg(1)
    # Clear input line
    misc_tools.pos_print(5,43," "*(misc_tools.get_terminal_width()-46))

def scan_target(ip_address,subnet_mask, scan_flags,output_flags):
    """ Scan target save result in scan_res"""
    global scan_res
    # Add the path to nmap.exe if running on windows.
    # THIS PATH MIGHT NEED TO BE ALTERED FOR YOUR SYSTEM
    if WINDOWS:
        scan_obj = nmap.PortScanner(nmap_search_path = [r"C:\Program Files (x86)\Nmap\nmap.exe",])
    else:
        scan_obj = nmap.PortScanner()

    host_str = ip_address  + "/" + subnet_mask
    # Update status message
    set_status_msg(f"Scanning {host_str}")
    print_status_msg()

    scan_obj.scan(host_str, arguments=scan_flag_str+output_flag_str)
    scan_res = scan_obj[ip_address]

    # Update status message
    set_status_msg(f"Scan of {host_str} is complete")
    print_status_msg(1)

def set_scan_flags():
    """
    User input which flags to select
    """
    set_status_msg("Running set_scan_flags")
    print_status_msg(1)

def set_output_flags():
    """ 
    User input which output flags to select
    """
    set_status_msg("Running set_output_flags")
    print_status_msg(1)

def scan_ip_address():
    """ 
    Call the scan_target function
    """
    scan_target(ip_addr_str, subnet_mask_str, scan_flag_str, output_flag_str)

def display_scan_result():
    """
    Print the result of the scan to the screen
    """
    set_status_msg("Printing the result from scan")
    print_status_msg()
    scan_result =[]
    # Format scan result data to desired output
    for line in range(50):
        scan_result.append(("line: ",str(line).rjust(3)))

    # Send formated data to ouput window
    output_window(scan_result, active=True)
    output_window([("",)],False)

def save_scan_result():
    """ 
    Save scan result to file
    """
    set_status_msg("Running save_scan_result")
    print_status_msg(1)

def load_scan_settings():
    """ 
    Load settings from file
    """
    set_status_msg("Running load_scan settings")
    print_status_msg(1)

def save_scan_settings():
    """
    Save settings from file
    """
    set_status_msg("Running save_scan settings")
    print_status_msg(1)

def display_help():
    """ 
    Print help to the screen
    """
    set_status_msg("Running display_help")
    print_status_msg(1)

def print_status_msg(delay=0):
    """ 
    Print value of status_msg below menu
    """
    # print status_msg
    print(Fore.GREEN)
    misc_tools.print_window([("Status: "+status_msg,)],1,1,misc_tools.get_terminal_width(),True)
    print(Fore.RESET)
    time.sleep(delay)

def output_window(text_list:list,active:bool):
    """ 
    Prints provided list of tuples of strings in output window under status message
    If active then scroll with up and down keys, quit with Q
    """
    max_height = misc_tools.get_terminal_height()-7
    max_width = misc_tools.get_terminal_width()-44
    # If provided text is less then max_height lines long, append blank lines
    line_count = len(text_list)
    while line_count < max_height:
        text_list.append(("",))
        line_count +=1

    start_row = 0
    while True:
        output_text = text_list[start_row:start_row+max_height:]
        misc_tools.pos_print(1,1,Fore.LIGHTYELLOW_EX)
        misc_tools.print_window(output_text,4,42,max_width,True)
        misc_tools.pos_print(1,1,Fore.RESET)
        #if it's an active window
        if active:
            # Check if at top of text
            top_of_text = start_row == 0
            # Check if at end of text
            end_of_text = start_row+max_height == len(text_list)

            if not top_of_text:
                #Enable up arrow
                print(Fore.GREEN)
                misc_tools.pos_print(5, max_width+43,"^")
            else:
                #Disable up arrow
                print(Fore.RED)
                misc_tools.pos_print(5, max_width+43,"^")

            if not end_of_text:
                #Enable up arrow
                print(Fore.GREEN)
                misc_tools.pos_print(max_height+4, max_width+43,"V")
            else:
                #Disable up arrow
                print(Fore.RED)
                misc_tools.pos_print(max_height+4, max_width+43,"V")
            print(Fore.RESET)
            set_status_msg("Scroll using up and down arrows. Quit with Q")
            print_status_msg()
            nav = misc_tools.get_key()
            #if an arrow was pressed
            if nav == "\\xe0":
                sec_nav = misc_tools.get_key()
                if sec_nav == "H":
                    start_row -=1
                    start_row = max(start_row,0)
                elif sec_nav =="P":
                    start_row +=1
                    start_row =min(start_row, len(text_list)-max_height)
            elif nav =="Q":
                break

        else:
            #if not active window
            break

def settings_window():
    """ 
    Display the settings swindow
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
    misc_tools.pos_print(1,1,Fore.BLUE)
    misc_tools.print_window(setting_stats,4,1,40,True)
    misc_tools.pos_print(1,1,Fore.RESET)

def end_program():
    """ 
    Clears screen and quits to shell
    """
    misc_tools.clear_screen()
    misc_tools.stop_program()

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
        ("0", "Quit program", end_program),
        ("R", "Refresh sreen", misc_tools.clear_screen),
    ]

def main_menu():
    """ 
    Update status message, print menu and handle response
    """
    set_status_msg("Waiting for input. Select from main menu.")
    print_status_msg()
    # print menu and wait for user selection
    misc_tools.menu(MAIN_MENU_LIST,5,32,13,1,menu_header="Nmap Tools by SweJob")

def main():
    """ 
    Main program
    """
    # Clear Screen
    while True:
        misc_tools.clear_screen()
        output_window([("",)],False)
        # Print the settings window upper left corner
        settings_window()
        # Print any recieved status messages at the top, right of setting window
        print_status_msg(1)
        # Run main menu function
        main_menu()

if __name__ == "__main__":
    main()
