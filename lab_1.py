""" 
Laboration 1 - ITST24 , programmering för säkerhetstestare
Module for using nmap from python
Requirements:
1. Possible to save the result of the scan to a file
2. Use input/file to decide which ip-adress to scan
3. Menu where user choose what to do

Optional:
4. Developers imagination to add more functions in the tool

set_status_msg() - changes value of global variable _status_msg
print_status_msg(delay) - display a box with _status_msg. [delay] seconds pause after
end_program() - quits to shell and clears screen to avoid a cluttered shell
main_menu() - displays a main menu as described in the constant MAIN_MENU_LIST
"""

__version__ = "0.1"
__author__ = "Jonas Bergstedt"
import time
import nmap
from colorama import Fore
from swejob_tools import misc_tools
# defining some constants to be used
MAIN_MENU_START_ROW = 4
MAIN_MENU_START_COL = 1
MAIN_MENU_COLOR = Fore.MAGENTA
STATUS_MSG_START_ROW = 1
STATUS_MSG_START_COL = 1
STATUS_MSG_COLOR = Fore.GREEN


# defining some global variables
_status_msg = "Ready"

def set_status_msg(msg: str):
    """
    Set status_msg to msg or 'Ready' if msg is empty 
    """
    global _status_msg
    if msg == "":
        _status_msg = "Ready"
    else:
        _status_msg = msg

def print_status_msg(delay :int = 0):
    """ 
    Print value of status_msg below menu
    """
    # print status_msg
    print(STATUS_MSG_COLOR)
    misc_tools.print_window(
        [("Status: "+_status_msg,)],
        STATUS_MSG_START_ROW,
        STATUS_MSG_START_COL,
        misc_tools.get_terminal_width()-2,True)

    print(Fore.RESET)
    time.sleep(delay)

def end_program():
    """ 
    Clears screen and quits to shell
    """
    misc_tools.clear_screen()
    misc_tools.stop_program()

def ip_address_menu():
    """ 
    Display a menu for IP address handling
    """    
    misc_tools.clear_screen()
    set_status_msg("Waiting for input. Select from IP address menu")
    print_status_msg()
    ADDRESS_MENU_LIST =[
        # ("1", "List IP adresses", display_ip_adresses),
        # ("2", "Add IP address", add_ip_address),
        # ("3", "Remove IP address", remove_ip_address),
        # ("4", "Save IP adresses to file", save_ip_addresses),
        # ("5", "Load IP adresses from file", load_ip_adresses),
        ("0", "Return to main menu", misc_tools.end_menu)
    ]
    selection = ""
    while selection != "0":
        selection = misc_tools.menu(ADDRESS_MENU_LIST,5,32,4,1,menu_header="IP address menu")
    
# Constant with list of tuple containing:
# Selector, menu item and funcion to run
# Lines commented out are yet to be implemented
MAIN_MENU_LIST = [
        ("1", "IP address(es)...", ip_address_menu),
        # ("2", "Arguments and flags...", args_menu),
        # ("3", "Scan", scan_menu),
        # ("4", "Scan result...", display_scan_result),
        # ("5", "Save scan settings to file", save_scan_settings),
        # ("6", "Load scan settings from file", load_scan_settings),
        # ("7", "Help",display_help),
        ("Q", "Quit program", misc_tools.end_menu),
        # ("R", "Refresh sreen", misc_tools.clear_screen),
    ]

def main_menu():
    """ 
    Print main menu and handle response
    """
    set_status_msg("Waiting for input. Select from main menu.")
    print_status_msg()
    # print menu and wait for user selection
    result = misc_tools.menu(MAIN_MENU_LIST,5,32,4,1,menu_header="Laboration 1 by SweJob")
    return result

def main():
    """
    Laboration 1
    """
    misc_tools.clear_screen()
    menu_selection = ""
    while menu_selection != "Q":
        print_status_msg()
        menu_selection = main_menu()
    end_program()
# If this module is run directly, run the main function
if __name__ == "__main__":
    main()
