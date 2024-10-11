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
# import nmap
from colorama import Fore
from swejob_tools import misc_tools
# defining some constants to be used
MENU_WIDTH = 38

MAIN_MENU_START_ROW = 4
MAIN_MENU_START_COL = 1
MAIN_MENU_COLOR = Fore.MAGENTA

ADDRESS_MENU_START_ROW = 4
ADDRESS_MENU_START_COL = 1
ADDRESS_COLOR = Fore.MAGENTA

STATUS_MSG_START_ROW = 1
STATUS_MSG_START_COL = 1
STATUS_MSG_COLOR = Fore.GREEN

OUTPUT_WINDOW_COLOR = Fore.YELLOW

IP_FILE_EXT = ".ipfile"


# defining some global variables
_ip_addresses = {"127.0.0.1/32"}
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

def output_window(text_list:list,active:bool):
    """ 
    Prints provided list of tuples of strings in output window under status message
    If active then scroll with up and down keys, quit with Q
    """
    max_height = misc_tools.get_terminal_height()-7
    max_width = misc_tools.get_terminal_width()-MENU_WIDTH-5
    # If provided text is less then max_height lines long, append blank lines
    line_count = len(text_list)
    while line_count < max_height:
        text_list.append(("",))
        line_count +=1

    start_row = 0
    while True:
        output_text = text_list[start_row:start_row+max_height:]
        misc_tools.pos_print(1,1,OUTPUT_WINDOW_COLOR)
        misc_tools.print_window(output_text,4,42,max_width,True)
        misc_tools.pos_print(1,1,Fore.RESET)
        #if it's an active window
        if active and len(text_list) > max_height:
            # Check if at top of text
            top_of_text = start_row == 0
            # Check if at end of text
            end_of_text = start_row+max_height == len(text_list)

            if not top_of_text:
                #Enable up arrow
                misc_tools.pos_print(5,max_width+43,Fore.GREEN+"^")
            else:
                #Disable up arrow
                misc_tools.pos_print(5,max_width+43,Fore.RED+"^")

            if not end_of_text:
                #Enable up arrow
                misc_tools.pos_print(max_height+4, max_width+43,Fore.GREEN+"V")
            else:
                #Disable up arrow
                misc_tools.pos_print(max_height+4, max_width+43,Fore.RED+"V")
            print(Fore.RESET)
            set_status_msg("Scroll using up and down arrows. Quit with Q")
            print_status_msg()
            nav = misc_tools.get_key(False)
            #if an arrow was pressed
            if nav == "\\xe0":
                sec_nav = misc_tools.get_key(False)
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

def display_ip_addresses():
    """ 
    Displays the list of IP Addresses
    """
    ip_address_list =[]
    for ip_address in _ip_addresses:
        ip_address_list.append((ip_address.ljust(17),))
    output_window(ip_address_list,True)

def input_ip_address():
    """ 
    Get IP address with optional mask from user
    Return IP address with optional mask
    """
    valid_ip_addr = False
    valid_mask = False
    output_window(
        ["Enter IP address and [optional] mask [aaa.bbb.ccc.ddd][/0-32]."],
        False)
    # loop until valid adress is entered
    while not (valid_ip_addr and valid_mask):
        print_status_msg()
        # Clear previous entry
        misc_tools.pos_print(6,43," "*(misc_tools.get_terminal_width()-46))
        # Get input , prompt under status message
        user_ip_addr = input("\x1b[6;43HIP-address[/mask]: ")
        #check if entered adress minus any mask provided is valid
        valid_ip_addr = misc_tools.is_valid_ip_address(user_ip_addr.split("/")[0])
        if not valid_ip_addr:
            set_status_msg(f"'{user_ip_addr.split("/")[0]}' is not a valid IP-address")
        if "/" in user_ip_addr:
        # check to see if anything came after "/"
            if len(user_ip_addr.split("/")[1]) > 0:
                # If that was a number between 0 and 32
                subnet_mask_str = user_ip_addr.split("/")[1]
                if not(subnet_mask_str.isdigit() and int(subnet_mask_str) in range(0,33)):
                    set_status_msg(f"'{user_ip_addr.split("/")[1]}' is not a valid subnet mask")
                    valid_mask = False
                else:
                    valid_mask = True
            else:
                set_status_msg("No subnet value provided after divider ('/')")
                valid_mask = False
        else:
            set_status_msg("No mask provided. The default 32-bit mask will be used")
            subnet_mask_str = "32"
            user_ip_addr = user_ip_addr.split("/")[0] + "/32"
            valid_mask = True
            
    # Clear input line
    misc_tools.pos_print(5,43," "*(misc_tools.get_terminal_width()-MENU_WIDTH-6))
    misc_tools.pos_print(6,43," "*(misc_tools.get_terminal_width()-MENU_WIDTH-6))
    return user_ip_addr

def add_ip_address():
    """ 
    Get IP address and mask from user
    Setting global variables to valid ip_string and mask
    """
    set_status_msg("Enter IP adress to add")
    print_status_msg()
    _ip_addresses.add(input_ip_address())
    display_ip_addresses()

def remove_ip_address():
    set_status_msg("Enter IP adress to remove")
    print_status_msg()
    # Add a check if IP address in the list or not
    try:
        _ip_addresses.remove(input_ip_address())
    except KeyError:
        set_status_msg("IP address not in list. Enter IP adress to remove")
        print_status_msg()
    display_ip_addresses()

def save_ip_addresses():
    """ 
    Save the list of IP adressess in a file
    """
    # List files with .ipfile - extension
    # Get file name from user
    # Check if file exists. Overwrite?
    # Write file
    
def load_ip_addresses():
    """ 
    Load list of IP adressess from a file
    """
    # List files with .ipfile - extension
    # Let user select
    # Read file
    
ADDRESS_MENU_LIST =[
        ("1", "Add IP address", add_ip_address),
        ("2", "Remove IP address", remove_ip_address),
        ("3", "Save IP adresses to file", save_ip_addresses),
        # ("4", "Load IP adresses from file", load_ip_adresses),
        ("0", "Return to main menu", misc_tools.nothing),
        ("Q", "Quit program", end_program)
    ]

def ip_address_menu():
    """ 
    Display a menu for IP address handling
    """
    misc_tools.clear_screen()
    selection = ""
    while selection != "0":
        display_ip_addresses()
        set_status_msg("Waiting for input. Select from IP address menu")
        print_status_msg()
        print(ADDRESS_COLOR)
        selection = misc_tools.menu(
            ADDRESS_MENU_LIST,
            5,
            MENU_WIDTH-6,
            ADDRESS_MENU_START_ROW,
            ADDRESS_MENU_START_COL,
            menu_header="IP address menu")
        print(Fore.RESET)

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
        ("Q", "Quit program", misc_tools.nothing),
        # ("R", "Refresh screen", misc_tools.clear_screen),
    ]

def main_menu():
    """ 
    Print main menu and handle response
    """
    set_status_msg("Waiting for input. Select from main menu.")
    print_status_msg()
    # print menu and wait for user selection
    print(MAIN_MENU_COLOR)
    result = misc_tools.menu(
        MAIN_MENU_LIST,
        5,
        MENU_WIDTH-6,
        4,
        1,
        menu_header="Laboration 1 by SweJob")

    print(Fore.RESET)
    return result

def main():
    """
    Laboration 1
    """

    menu_selection = ""
    while menu_selection != "Q":
        misc_tools.clear_screen()
        print_status_msg()
        menu_selection = main_menu()
    end_program()
# If this module is run directly, run the main function
if __name__ == "__main__":
    main()
