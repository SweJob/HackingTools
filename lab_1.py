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
from pathlib import Path
from pathvalidate import ValidationError, validate_filename
from colorama import Fore,Style,Back
from swejob_tools import misc_tools
# Constants
MENU_WIDTH = 38

MAIN_MENU_START_ROW = 4
MAIN_MENU_START_COL = 1
MAIN_MENU_COLOR = Fore.MAGENTA

ADDRESS_MENU_START_ROW = 4
ADDRESS_MENU_START_COL = 1
ADDRESS_COLOR = Fore.MAGENTA

STATUS_MSG_START_ROW = 1
STATUS_MSG_START_COL = 1
STATUS_MSG_MAX_WIDTH = 140
STATUS_MSG_COLOR = Fore.GREEN

OUTPUT_WINDOW_COLOR = Fore.YELLOW

IP_ADR_LIST_START_ROW = 4
IP_ADR_LIST_START_COL = 41
IP_ADR_LIST_MAX_HEIGHT= 30
IP_ADR_LIST_MAX_WIDTH = 100

IP_ADR_INPUT_START_ROW = 4
IP_ADR_INPUT_START_COL = 1
IP_ADR_INPUT_MAX_HEIGHT = 3
IP_ADR_INPUT_MAX_WIDTH = STATUS_MSG_MAX_WIDTH

FILE_INPUT_START_ROW =  4
FILE_INPUT_START_COL = 41
FILE_INPUT_MAX_HEIGHT = 3
FILE_INPUT_MAX_WIDTH = 100

FILE_LIST_START_ROW = 7
FILE_LIST_START_COL = 41
FILE_LIST_MAX_HEIGHT= 10
FILE_LIST_MAX_WIDTH = 100

IP_FILE_EXT = ".ipfile"

# Global variables
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
        min(STATUS_MSG_MAX_WIDTH,misc_tools.get_terminal_width()-2),
        True)

    print(Fore.RESET)
    time.sleep(delay)

def end_program():
    """ 
    Clears screen and quits to shell
    """
    misc_tools.clear_screen()
    misc_tools.stop_program()

def output_window(
    text_list:list,
    start_row:int,
    start_col: int,
    height: int,
    width: int,
    active:bool = False,
    select_list:bool = False):
    """ 
    Prints provided list of tuples of strings in output window under status message
    If active then scroll with pgup and pgdown keys, quit with Q
    If select_list, automatically active and select line within displayed part of list 
    with arrow up/downs. Enter to confirm selction. returns selected items id from text_list
    """
    max_height = min(height, misc_tools.get_terminal_height() -start_row-2)
    max_width = min(width,misc_tools.get_terminal_width()-start_col-2)
    # If provided text (+ 2 for the frame) is less then max_height lines long, append blank lines
    line_count = len(text_list) + 2
    while line_count < max_height:
        text_list.append(("",))
        line_count +=1

    row_counter = 0
    selected_line = 0
    while True:
        output_text = text_list[row_counter:row_counter+max_height-2:]
        misc_tools.pos_print(1,1,OUTPUT_WINDOW_COLOR)
        misc_tools.print_window(output_text,start_row,start_col,max_width,True)
        misc_tools.pos_print(1,1,Fore.RESET)
        #if it's an active window
        if select_list or (active and len(text_list)>(max_height-2)):
            # Check if at top of text
            top_of_text = row_counter == 0
            # Check if at end of text
            end_of_text = row_counter + max_height-2 == len(text_list)
            # print selector
            misc_tools.pos_print(1,1,Fore.BLACK+Back.WHITE+Style.BRIGHT)
            misc_tools.pos_print(start_row+1+selected_line, start_col+max_width-5,"<--")
            misc_tools.pos_print(1,1,Fore.RESET+Back.RESET+Style.RESET_ALL)

            if not top_of_text:
                #Enable up arrow
                misc_tools.pos_print(start_row+1, max_width+42, Fore.GREEN + "^")
            else:
                #Disable up arrow
                misc_tools.pos_print(start_row+1, max_width+42, Fore.RED + "^")

            if not end_of_text:
                #Enable up arrow
                misc_tools.pos_print(start_row+max_height-2, start_col+max_width+1, Fore.GREEN+"V")
            else:
                #Disable up arrow
                misc_tools.pos_print(start_row+max_height-2, start_col+max_width+1, Fore.RED+"V")
            print(Fore.RESET)
            msg = "Move selector with up/down arrow."
            if select_list:
                msg = msg + " . Select With Enter."
            msg = msg + " Any other key to quit!"
            set_status_msg(msg)
            print_status_msg()
            nav = misc_tools.get_key(False)
            if nav == "\\xe0":
                sec_nav = misc_tools.get_key(False)
                # set_status_msg(f"{nav} + {sec_nav} was pressed")
                # print_status_msg(1)
                if sec_nav == "H" and select_list:
                    # arrow up
                    if selected_line == 0:
                        # at top of window
                        row_counter -=1
                        row_counter = max(row_counter,0)
                    else:
                        # move up in window
                        selected_line -=1
                        selected_line = max(selected_line,0)

                elif sec_nav == "P" and select_list:
                    # arrow down
                    if selected_line > max_height-4:
                        # at bottom of window
                        row_counter +=1
                        row_counter =min(row_counter, len(text_list)-(max_height-2))
                    else:
                        # move down in window
                        selected_line +=1
                        selected_line = min(selected_line,(max_height-3))
            elif nav =="\\r" and select_list:
                # Enter
                return row_counter+selected_line
            else:
                return None

        else:
            #if not active window
            return None

def display_ip_addresses():
    """ 
    Displays the list of IP Addresses
    """
    ip_address_list =[]
    for ip_address in sorted(_ip_addresses):
        ip_address_list.append((ip_address.strip(),))
    output_window(
        ip_address_list,
        IP_ADR_LIST_START_ROW,
        IP_ADR_LIST_START_COL,
        IP_ADR_LIST_MAX_HEIGHT,
        IP_ADR_LIST_MAX_WIDTH,
        True,
        False)

def input_ip_address():
    """ 
    Get IP address with optional mask from user
    Return IP address with optional mask
    """
    valid_ip_addr = False
    valid_mask = False
    misc_tools.clear_screen()
    set_status_msg("Enter IP address and [optional] mask [aaa.bbb.ccc.ddd][/0-32].")
    # loop until valid adress is entered
    while not (valid_ip_addr and valid_mask):
        print_status_msg()
        # Get input , prompt under status message
        output_window(
            [tuple()],
            IP_ADR_INPUT_START_ROW,
            IP_ADR_INPUT_START_COL,
            IP_ADR_INPUT_MAX_HEIGHT,
            IP_ADR_INPUT_MAX_WIDTH,
            False, False)
        user_ip_addr = input(
            f"\x1b[{IP_ADR_INPUT_START_ROW+1};{IP_ADR_INPUT_START_COL+1}HIP-address[/mask]: ")
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
    misc_tools.pos_print(6,43," "*(misc_tools.get_terminal_width()-MENU_WIDTH-6))
    return user_ip_addr

def add_ip_address():
    """ 
    Get IP address and mask from user
    Setting global variables to valid ip_string and mask
    """
    misc_tools.clear_screen()
    set_status_msg("Enter IP adress to add")
    print_status_msg()
    _ip_addresses.add(input_ip_address())
    display_ip_addresses()

def remove_ip_address():
    """ 
    Delete IP adress from list
    """
    set_status_msg("Enter IP adress to remove")
    print_status_msg()
    # Add a check if IP address in the list or not
    try:
        _ip_addresses.remove(input_ip_address())
    except KeyError:
        set_status_msg("IP address not in list. Enter IP adress to remove")
        print_status_msg()
    display_ip_addresses()

def list_files(directory: str = ".", file_name: str = "*", extension: str =".*"):
    """ 
    create and return a list of files with the extension provided or all files
    """
    my_dir = Path(directory +"/")
    search_for = file_name+extension
    file_list = sorted(my_dir.glob(search_for))
    return file_list

def file_exists(file_path__name: str):
    """
    Return true if file exists
    """
    checked_file = Path(file_path__name).is_file()
    return checked_file

def display_file_list(
    extension: str,
    selectable: bool = False,
    start_row=FILE_LIST_START_ROW,
    start_col=FILE_LIST_START_COL):
    """
    Show a list of files in current directory
    Select file with arrow keys and enter
    Tab to enter a filename instead    
    """
    set_status_msg(f"List of existing files with the extension '{extension}")
    print_status_msg()
    ipfile_list = list_files(extension=extension)
    # create a list of tuple of strings to be used in the file_list_window
    display_list = []
    for file_obj in ipfile_list:
        file_name = file_obj.name
        display_list.append((file_name.ljust(20),))
    selected_file = output_window(
        display_list,
        start_row,
        start_col,
        FILE_LIST_MAX_HEIGHT,
        FILE_LIST_MAX_WIDTH,
        False,
        selectable)
    if selectable and not selected_file is None:
        file_name = display_list[selected_file][0]
        return file_name
    return None

def get_file_name():
    """
    Return a filename entered by user
    """
    # Get input , prompt under status message
    output_window(
        [tuple()],
        IP_ADR_INPUT_START_ROW,
        IP_ADR_INPUT_START_COL,
        IP_ADR_INPUT_MAX_HEIGHT,
        IP_ADR_INPUT_MAX_WIDTH,
        False, False)
    file_name = input(f"\x1b[{IP_ADR_INPUT_START_ROW+1};{IP_ADR_INPUT_START_COL+1}HFilename: ")
    return file_name

def is_valid_file_name(file_name:str):
    """ 
    Checks if argument is a valid filename to use
    """
    try:
        validate_filename(file_name)
    except ValidationError:
        return False
    return True

def save_ip_addresses():
    """ 
    Save the list of IP adressess in a file in the current directory
    """
    misc_tools.clear_screen()
    # List files with .ipfile - extension
    display_file_list(f"{IP_FILE_EXT}")
    # Enter a filename to save the settings to
    set_status_msg("Enter filename to save IP-addresses to ('.ipfile' will be the extension)")
    print_status_msg()
    valid_filename = False
    # Check if entered text is a valid filename
    while not valid_filename:
        file_name = get_file_name() + IP_FILE_EXT
        valid_filename = is_valid_file_name(file_name)
        if not valid_filename:
            set_status_msg(f"'{file_name}' is not a valid filename. Try again.")

    # Check if file already exists
    if file_exists(file_name):
        set_status_msg(f"'{file_name}' already exists. Press Y to overwrite, other key to cancel")
        print_status_msg()
        answer = misc_tools.get_key()
        if answer != "Y":
            set_status_msg("Cancelling saving IP-addresses to file")
            print_status_msg(1)
            return

    # Try writing to file
    set_status_msg(f"Writing IP-addresses to '{file_name}'")
    print_status_msg()
    try:
        with open(file_name,'w') as ip_file:
            for address in _ip_addresses:
                ip_file.write(address+'\n')
    except:
        set_status_msg(f"Something went wrong writing IP-addresses to '{file_name}'")
    print_status_msg(1)

def load_ip_file(file_name):
    """ 
    Load IP-adresses from a .ipfile to global variable _ip_adresses
    """
    try:
        with open(file_name, 'r') as ip_file:
            local_address_set =set([])
            for line in ip_file:
                local_address_set.add(line)
            global _ip_addresses
            _ip_addresses = local_address_set
    except:
        set_status_msg(f"Something went wrong when reading from {file_name}")

def load_ip_addresses():
    """ 
    Load list of IP adressess from a file
    """
    # List files with .ipfile - extension
    # Let user select
    # Read file
    misc_tools.clear_screen()
    set_status_msg("Select file to load IP-addresses from")
    print_status_msg()
    selected_file = display_file_list(
                        extension=IP_FILE_EXT,
                        selectable=True,
                        start_row=4,
                        start_col=1)
    if not selected_file is None:
        load_ip_file(selected_file)

ADDRESS_MENU_LIST =[
        ("1", "Add IP address", add_ip_address),
        ("2", "Remove IP address", remove_ip_address),
        ("3", "Save IP adresses to file", save_ip_addresses),
        ("4", "Load IP adresses from file", load_ip_addresses),
        ("0", "Return to main menu", misc_tools.nothing),
        ("Q", "Quit program", end_program)
    ]

def ip_address_menu():
    """ 
    Display a menu for IP address handling
    """
    selection = ""
    while selection != "0":
        misc_tools.clear_screen()
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
