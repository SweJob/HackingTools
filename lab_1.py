""" 
Laboration 1 - Kurs "Programmering för säkerhetstestare", ITST24 , IT-Högskolan
Module for using nmap from python
Requirements:
1. Possible to save the result of the scan to a file
2. Use input/file to decide which ip-adress to scan
3. Menu where user choose what to do

Optional:
4. Developers imagination to add more functions in the tool
"""
__version__ = "0.2"
__author__ = "Jonas Bergstedt"
import time
import json
from pathlib import Path
import nmap
from pathvalidate import ValidationError, validate_filename
from colorama import Fore,Style,Back
from swejob_tools import misc_tools

# Constants
TERM_MIN_ROW = 28
TERM_MIN_COL = 90

MENU_WIDTH = 38
MENU_START_ROW = 5
MENU_START_COL = 1
MENU_COLOR = Fore.MAGENTA

STATUS_MSG_START_ROW = 1
STATUS_MSG_START_COL = 1
STATUS_MSG_MAX_WIDTH = 140
STATUS_MSG_COLOR = Fore.GREEN

OUTPUT_WINDOW_COLOR = Fore.YELLOW

FILE_INPUT_START_ROW =  17
FILE_INPUT_START_COL = 1
FILE_INPUT_MAX_HEIGHT = 3
FILE_INPUT_MAX_WIDTH = 100

FILE_LIST_START_ROW = 5
FILE_LIST_START_COL = 1
FILE_LIST_MAX_HEIGHT= 10
FILE_LIST_MAX_WIDTH = 100

IP_ADR_LIST_START_ROW = 5
IP_ADR_LIST_START_COL = 41
IP_ADR_LIST_MAX_HEIGHT= 30
IP_ADR_LIST_MAX_WIDTH = 100

IP_ADR_INPUT_START_ROW = 5
IP_ADR_INPUT_START_COL = 1
IP_ADR_INPUT_MAX_HEIGHT = 3
IP_ADR_INPUT_MAX_WIDTH = STATUS_MSG_MAX_WIDTH

IP_FILE_EXT = ".ip.txt"

ARGS_LIST_START_ROW = 5
ARGS_LIST_START_COL = 1
ARGS_LIST_MAX_HEIGHT = 21
ARGS_LIST_MAX_WIDTH = 75

ARG_FILE_EXT =".arg.txt"

SCAN_RESULT_LIST_START_ROW = 5
SCAN_RESULT_LIST_START_COL = 1
SCAN_RESULT_LIST_MAX_HEIGHT = 30
SCAN_RESULT_LIST_MAX_WIDTH = 100

SCAN_RESULT_FILE_EXT = ".scans.json"

# Global variables
_ip_addresses: set = {"127.0.0.1/32"}
_status_msg: str = "Ready"
_arg_string: str = ""
_port_str: str = ""
_scan_results: set = []
_addr_saved: bool = True
_args_saved: bool = True
_scan_saved: bool = True

def check_terminal_size():
    misc_tools.clear_screen()
    while not misc_tools.minimal_terminal_size(TERM_MIN_ROW,TERM_MIN_ROW):
        height = misc_tools.get_terminal_height()
        width = misc_tools.get_terminal_width()
        to_small_msg = f"Please resize terminal. Current size: {height}*{width}. Minimum size: {TERM_MIN_ROW}*{TERM_MIN_COL}"
        set_status_msg(to_small_msg)
        print_status_msg(0.3)

def set_status_msg(msg: str):
    """ Set status_msg to msg or 'Ready' if msg is empty """
    global _status_msg
    if msg == "":
        _status_msg = "Ready"
    else:
        _status_msg = msg

def print_status_msg(delay :int = 0):
    """ 
    Print value of status_msg below menu
    """
    ip_save_state = "IP adresses: "
    if _addr_saved:
        ip_save_state += "Saved"
    else:
        ip_save_state += "NOT saved"
    arg_save_state = "Arguments: "
    if _args_saved:
        arg_save_state += "Saved"
    else:
        arg_save_state += "NOT saved"
    scan_save_state = "Scans: "
    if _scan_saved:
        scan_save_state += "Saved"
    else:
        scan_save_state += "NOT saved"

    print(STATUS_MSG_COLOR)
    status_msg_list = [
        (ip_save_state, "   ", arg_save_state, "   ", scan_save_state),
        (_status_msg,)
    ]
    misc_tools.print_window(status_msg_list,
        STATUS_MSG_START_ROW,
        STATUS_MSG_START_COL,
        min(STATUS_MSG_MAX_WIDTH,misc_tools.get_terminal_width()-2),
        True)

    print(Fore.RESET)
    time.sleep(delay)

def end_program():
    """ Reset terminal formatting, clear screen and quit to shell """
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)
    misc_tools.clear_screen()
    misc_tools.stop_program()

def output_window(
    text_list:list,
    start_row:int,
    start_col: int,
    height: int,
    width: int,
    active:bool = False,
    select_list:bool = False,
    start_line:int =0):
    """ 
    Prints provided list of tuples of strings in output window under status message
    If active then scroll with pgup and pgdown keys, quit with Q
    If select_list, automatically active and select line within displayed part of list 
    with arrow up/downs. Enter to confirm selction. returns selected items id from text_list
    """
    max_height = min(height, misc_tools.get_terminal_height() -start_row-2)
    max_width = min(width,misc_tools.get_terminal_width()-start_col-2)
    # If provided text (+ 2 for the frame) is less then max_height lines long, append blank lines
    real_lines = len(text_list)
    line_count =  real_lines + 2
    while line_count < max_height:
        text_list.append(("",))
        line_count +=1
    row_counter = 0
    selected_line = start_line
    while True:
        output_text = text_list[row_counter:row_counter+max_height-2:]
        misc_tools.pos_print(1,1,OUTPUT_WINDOW_COLOR)
        misc_tools.print_window(output_text,start_row,start_col,max_width,True)
        misc_tools.pos_print(1,1,Fore.RESET)
        #if it's an active window
        if select_list or active:
            # Check if at top of text
            top_of_text = row_counter == 0
            # Check if at end of text
            end_of_text = row_counter + max_height -2 >= real_lines
            if select_list:
                # print selector
                misc_tools.pos_print(1,1,Fore.BLACK+Back.WHITE+Style.BRIGHT)
                misc_tools.pos_print(start_row+1+selected_line, start_col+max_width-5,"<--")
                misc_tools.pos_print(1,1,Fore.RESET+Back.RESET+Style.RESET_ALL)
            if not top_of_text:
                #Enable up arrow
                misc_tools.pos_print(start_row+1, start_col+max_width+1, Fore.GREEN + "^")
            else:
                #Disable up arrow
                misc_tools.pos_print(start_row+1, start_col+max_width+1, Fore.RED + "^")
            if not end_of_text:
                #Enable down arrow
                misc_tools.pos_print(start_row+max_height-2, start_col+max_width+1, Fore.GREEN+"V")
            else:
                #Disable down arrow
                misc_tools.pos_print(start_row+max_height-2, start_col+max_width+1, Fore.RED+"V")
            print(Fore.RESET)
            msg = "Move with up/down arrow."
            if select_list:
                msg = msg + " Select With Space or Enter."
            msg = msg + " Any other key to exit scroll window!"
            set_status_msg(msg)
            print_status_msg()
            misc_tools.pos_print(start_row+selected_line,start_col+1,"")
            if misc_tools.is_windows():
                nav = misc_tools.get_key()
                if nav == "\\xe0":
                    sec_nav = misc_tools.get_key()
                    key_pressed = ""           
                    if sec_nav == "H":
                        key_pressed = "UP"
                    elif sec_nav == "P":
                        key_pressed = "DOWN"
                    else:
                        key_pressed = "OTHER"
                elif nav == "\\r":
                    key_pressed = "ENTER"
                elif nav == " ":
                    key_pressed = "SPACE"
                else:
                    key_pressed = "OTHER"
            else:
                # Key handling in not-windows, FIXME: Arrows and Enter not correctly handled
                nav = misc_tools.get_key(test=True)
                if nav[0] == "\x1b":
                    sec_nav = nav[2]
                    key_pressed = ""
                    if sec_nav == "A":
                        key_pressed = "UP"
                    elif sec_nav == "B":
                        key_pressed = "DOWN"
                    else:
                        key_pressed = "OTHER"
                elif nav[0] == "\n":
                    key_pressed = "ENTER"
                elif nav[0] == " ":
                    key_pressed = "SPACE"
                else:
                    key_pressed = "OTHER"

            if key_pressed == "UP":
                # arrow up
                if select_list:
                    # if it's a selectable list
                    if selected_line == 0:
                        # at top of window
                        row_counter -=1
                        row_counter = max(row_counter,0)
                    else:
                        # move up in window
                        selected_line -=1
                        selected_line = max(selected_line,0)
                else:
                    # move up
                    row_counter -=1
                    row_counter = max(row_counter,0)
            elif key_pressed == "DOWN":
                # arrow down
                if select_list:
                    if selected_line == max_height-3:
                        # at bottom of window
                        row_counter +=1
                        row_counter =min(row_counter, real_lines-(max_height-2))
                    else:
                        # move down in window
                        selected_line +=1
                        selected_line = min(selected_line,real_lines-row_counter-1, max_height-3)
                else:
                    # move down
                    row_counter +=1
                    row_counter =min(row_counter, len(text_list)-(max_height-2))
            elif key_pressed in ("SPACE","ENTER") and select_list:
                # Space or Enter
                return row_counter+selected_line, selected_line
            else:
                return None, selected_line
        else:
            #if not active window
            return None, selected_line

def display_ip_addresses():
    """ Displays the list of IP Addresses """
    ip_address_list =[]
    for ip_address in sorted(_ip_addresses):
        ip_address_list.append((ip_address.strip(),))
    output_window(
        ip_address_list,
        IP_ADR_LIST_START_ROW,
        IP_ADR_LIST_START_COL,
        IP_ADR_LIST_MAX_HEIGHT,
        IP_ADR_LIST_MAX_WIDTH,
        False,
        False)

def input_ip_address():
    """ 
    Get IP address with optional mask from user,
    return IP address with mask (/32 if non provided)
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
    return user_ip_addr

def add_ip_address():
    """ Get IP address and mask from user. Setting global variables to valid ip_string and mask """
    misc_tools.clear_screen()
    set_status_msg("Enter IP adress to add")
    print_status_msg()
    _ip_addresses.add(input_ip_address())
    global _addr_saved
    _addr_saved = False
    display_ip_addresses()

def remove_ip_address():
    """ Delete IP adress from list """
    set_status_msg("Enter IP adress to remove")
    print_status_msg()
    # Add a check if IP address in the list or not
    try:
        _ip_addresses.remove(input_ip_address())
        global _addr_saved
        _addr_saved = False

    except KeyError:
        set_status_msg("IP address not in list. Enter IP adress to remove")
        print_status_msg()
    display_ip_addresses()

def list_files(directory: str = ".", file_name: str = "*", extension: str =".*"):
    """ Create and return a list of files with the extension provided or all files """
    my_dir = Path(directory +"/")
    search_for = file_name+extension
    file_list = sorted(my_dir.glob(search_for))
    return file_list

def file_exists(file_path__name: str):
    """ Return true if file exists """
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
    selected_file,selected_line = output_window(
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
    """ Return a filename entered by user """
    # Get input , prompt under status message
    output_window(
        [tuple()],
        FILE_INPUT_START_ROW,
        FILE_INPUT_START_COL,
        FILE_INPUT_MAX_HEIGHT,
        FILE_INPUT_MAX_WIDTH,
        False, False)
    file_name = input(f"\x1b[{FILE_INPUT_START_ROW+1};{FILE_INPUT_START_COL+1}HFilename: ")
    return file_name

def is_valid_file_name(file_name:str):
    """ Checks if argument is a valid filename to use """
    try:
        validate_filename(file_name)
    except ValidationError:
        return False
    return True

def save_ip_addresses():
    """ Save the list of IP adressess in a file in the current directory """
    misc_tools.clear_screen()
    # List files with .ipfile - extension
    display_file_list(f"{IP_FILE_EXT}")
    # Enter a filename to save the settings to
    set_status_msg(f"Enter filename to save IP-addresses to ('{IP_FILE_EXT}' is the extension)")
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
            return False
    # Try writing to file
    set_status_msg(f"Writing IP-addresses to '{file_name}'")
    print_status_msg()
    try:
        with open(file_name,'w', encoding="utf-8") as ip_file:
            for address in _ip_addresses:
                ip_file.write(address+'\n')
            global _addr_saved
            _addr_saved = True
    except:
        set_status_msg(f"Something went wrong writing IP-addresses to '{file_name}'")
        return False
    print_status_msg(1)
    return True

def load_ip_file(file_name):
    """ Load IP-adresses from a IP_FILE_EXT-file to global variable _ip_adresses """
    try:
        with open(file_name, 'r', encoding="utf-8") as ip_file:
            local_address_set =set([])
            for line in ip_file:
                local_address_set.add(line)
            global _ip_addresses
            _ip_addresses = local_address_set
            global _addr_saved
            _addr_saved = True
    except Exception as e:
        set_status_msg(f"Error {e} when reading IP-adresses from {file_name}")

def load_ip_addresses():
    """ 
    Dialogue to load list of IP adressess from a file
    """
    # List files with .ipfile - extension, let user select, read file
    misc_tools.clear_screen()
    set_status_msg("Select file to load IP-addresses from")
    print_status_msg()
    selected_file = display_file_list(
                        extension=IP_FILE_EXT,
                        selectable=True,
                        start_row=FILE_LIST_START_ROW,
                        start_col=FILE_LIST_START_COL)
    if not selected_file is None:
        load_ip_file(selected_file)

# Constant with list of tuple containing:
# Selector, menu item and funcion to run
ADDRESS_MENU_LIST =[
        ("1", "Add IP address", add_ip_address),
        ("2", "Remove IP address", remove_ip_address),
        ("3", "Save IP adresses to file", save_ip_addresses),
        ("4", "Load IP adresses from file", load_ip_addresses),
        ("0", "Return to main menu", misc_tools.nothing),
        ("Q", "Quit program", end_program)
    ]

def ip_address_menu():
    """ Display a menu for IP address handling """
    selection = ""
    while selection != "0":
        check_terminal_size()
        misc_tools.clear_screen()
        display_ip_addresses()
        set_status_msg("Waiting for input. Select from IP address menu")
        print_status_msg()
        print(MENU_COLOR)
        selection = misc_tools.menu(
            ADDRESS_MENU_LIST,
            5,
            MENU_WIDTH-6,
            MENU_START_ROW,
            MENU_START_COL,
            menu_header="IP address menu")
        print(Fore.RESET)

ARGS_LIST = [
        #("-sL".ljust(5),": List Scan - simply list targets to scan"),
        #("-sn".ljust(5),": Ping Scan - disable port scan"),
        ("-Pn".ljust(5),": Treat all hosts as online -- skip host discovery"),
        ("-PS".ljust(5),": TCP SYN"),
        ("-PA".ljust(5),": TCP ACK"),
        ("-PU".ljust(5),": UDP"),
        ("-PY".ljust(5),": SCTP"),
        ("-sS".ljust(5),": TCP SYN"),
        ("-sT".ljust(5),": Connect()"),
        ("-sA".ljust(5),": ACK"),
        #("-sW".ljust(5),": Window"),
        ("-sU".ljust(5),": UDP Scan"),
        ("-sN".ljust(5),": TCP Null"),
        ("-sF".ljust(5),": FIN"),
        #("-sX".ljust(5),": Xmas scans"),
        ("-O".ljust(5),": Enable OS detection"),
        ("-vv".ljust(5),": Verbose output"),
        ## Keep the next 2 lines in that order
        ("-p".ljust(5),": <port ranges>: Specify ports on next screen"),
        ("Finished selecting arguments",)
    ]
def get_ports():
    """ Return ports entered by user """
    # Get input , prompt under status message
    output_window(
        [tuple()],
        IP_ADR_INPUT_START_ROW,
        IP_ADR_INPUT_START_COL,
        IP_ADR_INPUT_MAX_HEIGHT,
        IP_ADR_INPUT_MAX_WIDTH,
        False, False)
    ports = input(f"\x1b[{IP_ADR_INPUT_START_ROW+1};{IP_ADR_INPUT_START_COL+1}HPorts: ")
    return ports

def select_arguments():
    """ 
    Display list of arguments and select which should be active or not 
    and provide extra info for those who needs it
    """
    # // NOTE: A risk of displaying problems if the terminal window is not high enough
    # Make a list of bools to keep track of which arguments are selected.
    # Set start values according to whats in the arguments

    global _arg_string
    global _port_str
    selected_arg_list =[]
    for arg in ARGS_LIST:
        flag = arg[0].strip()
        if _arg_string.find(flag) != -1:
            selected_arg_list.append(True)
        else:
            selected_arg_list.append(False)
    # remove last value in list, as it's not pointing to a flag
    selected_arg_list.pop()
    # Make a print_list with "Yes" for selected and "No" for not selected
    print_select_list =[]
    for selected in selected_arg_list:
        if selected:
            print_select_list.append(("Yes",))
        else:
            print_select_list.append(("No",))
    # Add a line for the Finish line in ARGS_LIST
    print_select_list.append(("-",))
    selection = 0
    lastline = 0
    while selection < len(ARGS_LIST)-1:
        check_terminal_size()
        #print the selection stat
        print(OUTPUT_WINDOW_COLOR)
        misc_tools.print_window(
            print_select_list,
            ARGS_LIST_START_ROW,
            ARGS_LIST_START_COL,
            width = 5,
            frame = True
        )
        misc_tools.pos_print(1,1,Fore.RESET)
        # print the arguments
        selection,lastline = output_window(
            ARGS_LIST,
            ARGS_LIST_START_ROW,
            ARGS_LIST_START_COL+5,
            len(ARGS_LIST)+2,
            ARGS_LIST_MAX_WIDTH,
            True,
            True,
            lastline
        )
        # If pressing any other key leave function instead of changing anything
        if selection is None:
            return None
        # selected anything but the last line
        if selection < len(ARGS_LIST)-1:
            # Toggle value of selected flag
            selected_arg_list[selection] = not selected_arg_list[selection]
             # Reset print_select_list with updated "Yes" / "No" for not choices
            print_select_list.clear()
            for selected in selected_arg_list:
                if selected:
                    print_select_list.append(("Yes",))
                else:
                    print_select_list.append(("No",))
                # Add a line for the Finish line in ARGS_LIST
            print_select_list.append(("-",))
    # You should get here when you selected the last line        
    if selected_arg_list[-1]:
        # If the last argument in list is selected ("-p") then go through this extra section
        #Enter a list or range of ports
        misc_tools.clear_screen()
        if len(_port_str) > 0:
            # If there are already ports in the argument
            set_status_msg(f"Ports already exist in the arguments: {_port_str}.Keep them (Y/N)")
            print_status_msg()
            keep = ""
            while keep not in ["Y","N"]:
                keep = misc_tools.get_key()
            if keep == "N":
                _port_str = ""
        set_status_msg(f"Enter port(s) to scan. CSV or range. Current ports:{_port_str}")
        print_status_msg()
        valid_port_string = False
        while not valid_port_string:
            entered_port_str=get_ports()
            if entered_port_str != "":
                for ports in entered_port_str.split(","):
                    for port in ports.split("-"):
                        if port.isdigit():
                            valid_port_string = True
            else:
                # If just enter was pressed, it's as not adding to the previous portstrin
                valid_port_string = True
        if len(_port_str) > 0 and len(entered_port_str) > 0:
            _port_str += ","
        _port_str += entered_port_str
    local_arg_str = ""
    for idx,selected in enumerate(selected_arg_list):
        if selected:
            local_arg_str = local_arg_str + ARGS_LIST[idx][0].strip() +" "
    _arg_string = local_arg_str
    global _args_saved
    _args_saved = False
    return local_arg_str

def save_args():
    """ Save arguments to file """
    misc_tools.clear_screen()
    if len(_arg_string) ==0 and len(_port_str) == 0:
        # If no arguments, cancel saving
        set_status_msg("No arguments or ports are set!")
        print_status_msg(1)
        return None
    # List files with .ipfile - extension
    display_file_list(f"{ARG_FILE_EXT}")
    # Enter a filename to save the settings to
    set_status_msg(f"Enter filename to save arguments to ('{ARG_FILE_EXT}' is the extension)")
    print_status_msg()
    valid_filename = False
    # Check if entered text is a valid filename
    while not valid_filename:
        file_name = get_file_name() + ARG_FILE_EXT
        valid_filename = is_valid_file_name(file_name)
        if not valid_filename:
            set_status_msg(f"'{file_name}' is not a valid filename. Try again.")
    # Check if file already exists
    if file_exists(file_name):
        set_status_msg(f"'{file_name}' already exists. Press Y to overwrite, other key to cancel")
        print_status_msg()
        answer = misc_tools.get_key()
        if answer != "Y":
            set_status_msg("Cancelling saving arguments to file")
            print_status_msg(1)
            return False
    # Try writing to file
    set_status_msg(f"Writing arguments to '{file_name}'")
    print_status_msg()
    try:
        with open(file_name,'w', encoding="utf-8") as arg_file:
            arg_file.write(_arg_string+"\n")
            arg_file.write(_port_str)
        global _args_saved
        _args_saved = True
    except:
        set_status_msg(f"Something went wrong writing arguments to '{file_name}'")
        return False
    print_status_msg(1)
    return True

def load_arg_file(file_name):
    """ Load arguments from a ARG_FILE_EXT-file to global variable _arg_string """
    try:
        with open(file_name, 'r', encoding="utf-8") as arg_file:
            global _arg_string
            global _port_str
            _arg_string = arg_file.readline().strip("\n")
            _port_str = arg_file.readline()
        global _args_saved
        _args_saved = True
    except Exception as e:
        set_status_msg(f"Error {e} reading arguments from {file_name}")
        print_status_msg(1)

def load_args():
    """ Dialogue to load arguments from a file """
    # List files with .ipfile - extension, let user select file, read file
    misc_tools.clear_screen()
    set_status_msg("Select file to load arguments from")
    print_status_msg()
    selected_file = display_file_list(
                        extension=ARG_FILE_EXT,
                        selectable=True,
                        start_row=FILE_LIST_START_ROW,
                        start_col=FILE_INPUT_START_COL)
    if not selected_file is None:
        load_arg_file(selected_file)

def clear_arguments():
    """ Erasing arguments from variable """
    set_status_msg("Do you want to erase arguement and ports from memory? (Y/N)")
    print_status_msg()
    if misc_tools.get_key() == "Y":
        global _arg_string
        _arg_string = ""
        global _port_str
        _port_str = ""
        global _args_saved
        _args_saved = True
        set_status_msg("Arguments and ports are erased!")
        print_status_msg(2)
# Constant with list of tuple containing:
# Selector, menu item and funcion to run
ARGS_MENU_LIST = [
        ("1", "Select arguments from list", select_arguments),
        ("2", "Save arguments to file", save_args),
        ("3", "Load arguments from file", load_args),
        ("9", "Clear all arguments", clear_arguments),
        ("0", "Return to main menu", misc_tools.nothing),
        ("Q", "Quit program", end_program)
    ]

def args_menu():
    """ Handle arguments to use """
    selection = ""
    while selection != "0":
        check_terminal_size()
        misc_tools.clear_screen()
        set_status_msg(f"Waiting for input. Select from menu. Args: {_arg_string} Ports: {_port_str}")
        print_status_msg()
        print(MENU_COLOR)
        selection = misc_tools.menu(
            ARGS_MENU_LIST,
            5,
            MENU_WIDTH-6,
            MENU_START_ROW,
            MENU_START_COL,
            menu_header="Arguments menu")
        print(Fore.RESET)

def scan_host(host,in_ports, in_arguments):
    """ Scanning host with arguments, returning the scan result"""
    set_status_msg(f"Scanning ports: {in_ports} at host: {host} with {in_arguments} as arguments.")
    print_status_msg(5)
    global _scan_saved
    try:
        if misc_tools.is_windows():
            nm = nmap.PortScanner(nmap_search_path= [r"C:\Program Files (x86)\Nmap\nmap.exe",])
        else:
            nm = nmap.PortScanner()
        nm.scan(hosts=host, arguments=in_arguments+in_ports)
    except nmap.PortScannerError():
        set_status_msg(f"Scan of {host} has failed. Arguments: {in_arguments} Ports: {in_ports}")
        print_status_msg(5)
    else:
        set_status_msg(f"Scan of {host} is done. Arguments{in_arguments} and ports{in_ports}")
        print_status_msg(5)
        all_hosts = nm.all_hosts()
        if len(all_hosts) < 1:
            result = {
                "hostnames":[{"name": "host did not respond"}],
                "addresses":{"ipv4" : f"{host.split("/")[0]}"},
                "status": {"state": "failed scan"}
            }
            _scan_results.append(result)
            _scan_saved = False
        else:
            for scanned_host in all_hosts:
                result = nm[scanned_host]
                _scan_results.append(result)
                _scan_saved = False

def scan():
    """ Scan the set of IP-adresses with the arguments. Save to list of scan results"""
    for scan_ip_address in _ip_addresses:
        scan_host(scan_ip_address,_port_str,_arg_string)

def display_scan_results():
    """ Print full scan result in scrollable window """
    scan_results_strings = []
    for scan_result in _scan_results:
        # Convert result dictionary to string
        json_scan_result = json.dumps(scan_result, indent=4)
        # Add each line in the json (split at "\n") as a new string in the list
        scan_results_strings = scan_results_strings + json_scan_result.split("\n")
        scan_results_strings.append("\n") # Add line after closing "{"
    scan_result_list =[]
    for line in scan_results_strings:
        scan_result_list.append((line,))
    output_window(
        scan_result_list,
        SCAN_RESULT_LIST_START_ROW,
        SCAN_RESULT_LIST_START_COL,
        SCAN_RESULT_LIST_MAX_HEIGHT,
        SCAN_RESULT_LIST_MAX_WIDTH,
        True,
        False)

def display_stripped_scan_results():
    """ Print stripped scan result in scrollable window """
    scan_results_strings =[]
    for scan_result in _scan_results:
        # Strip information from each scan_result and format it
        COLUMN = 12
        INDENT = "  "
        # Hostname  "hostnames": [{"name":}]
        hostname = "Hostname".ljust(COLUMN) + ": "+ scan_result["hostnames"][0]["name"]
        scan_results_strings.append(hostname)
        # IP Address "addresses": {"ipv4":}
        ip_address = "IP address".ljust(COLUMN) + ": "+ scan_result["addresses"]["ipv4"]
        scan_results_strings.append(ip_address)
        # Status    "status":{"state":}
        status = "Status".ljust(COLUMN) + ": "+ scan_result["status"]["state"]
        scan_results_strings.append(status)
        #If any tcp section, get some info and print it
        # TCP ports "tcp": {"portnummer":{state, reason, name, version}
        is_tcp = scan_result.get("tcp")
        if is_tcp is not None:
            scan_results_strings.append("TCP ports".ljust(COLUMN)+":")
            for tcp_port, port_info in is_tcp.items():
                scan_results_strings.append((INDENT + "Port#").ljust(COLUMN)+
                                            ": "+ 
                                            str(tcp_port).ljust(6)+
                                            port_info["name"])
                scan_results_strings.append((INDENT*2+
                                            "State").ljust(COLUMN)+
                                            ": "+
                                            port_info["state"])

        # UDP ports "udp": {"portnummer":{state, reason, name, version}
        is_udp = scan_result.get("udp")
        if is_udp is not None:
            scan_results_strings.append("UDP ports".ljust(COLUMN)+":")
            for udp_port, port_info in is_udp.items():
                scan_results_strings.append((INDENT +
                                             "Port#").ljust(COLUMN)+
                                            ": "+ str(udp_port).ljust(6)+
                                            port_info["name"])
                scan_results_strings.append((INDENT*2 +
                                            "State").ljust(COLUMN)+
                                            ": "+
                                            port_info["state"])
        # add empty line to last string of each scan result
        scan_results_strings.append("-----------------------------")
    scan_result_list =[]
    for line in scan_results_strings:
        scan_result_list.append((line,))
    output_window(
        scan_result_list,
        SCAN_RESULT_LIST_START_ROW,
        SCAN_RESULT_LIST_START_COL,
        SCAN_RESULT_LIST_MAX_HEIGHT,
        SCAN_RESULT_LIST_MAX_WIDTH,
        True,
        False)

def save_scan_results():
    """ Save the scan results as json objects in a file in the current directory """
    misc_tools.clear_screen()
    # List files with .ipfile - extension
    display_file_list(f"{SCAN_RESULT_FILE_EXT}")
    # Enter a filename to save the settings to
    set_status_msg(f"Enter filename to save results to ('{SCAN_RESULT_FILE_EXT}' is the extension)")
    print_status_msg()
    valid_filename = False
    # Check if entered text is a valid filename
    while not valid_filename:
        file_name = get_file_name() + SCAN_RESULT_FILE_EXT
        valid_filename = is_valid_file_name(file_name)
        if not valid_filename:
            set_status_msg(f"'{file_name}' is not a valid filename. Try again.")
    # Check if file already exists
    if file_exists(file_name):
        set_status_msg(f"'{file_name}' already exists. Press Y to overwrite, other key to cancel")
        print_status_msg()
        answer = misc_tools.get_key()
        if answer != "Y":
            set_status_msg("Cancelling saving scan results to file")
            print_status_msg(1)
            return False
    # Try writing to file as json
    set_status_msg(f"Writing scan results to '{file_name}'")
    print_status_msg()
    try:
        with open(file_name,'w', encoding="utf-8") as scan_result_file:
            for scan_result in _scan_results:
                json.dump(scan_result, scan_result_file)
                scan_result_file.write("\n")
        global _scan_saved
        _scan_saved = True
    except:
        set_status_msg(f"Something went wrong writing scan results to '{file_name}'")
        return False
    print_status_msg(1)
    return True

def load_scan_result_file(file_name):
    """ Load scan results from a SCAN_RESULT_FILE_EXT-file to global variable _ip_adresses """
    try:
        with open(file_name, 'r', encoding="utf-8") as scan_result_file:
            local_scan_results=[]
            for scan_result in(scan_result_file):
                scan_result_dict = json.loads(scan_result)
                local_scan_results.append(scan_result_dict)
            global _scan_results
            _scan_results = local_scan_results
            global _scan_saved
            _scan_saved = True
    except Exception as e:
        set_status_msg(f"Error {e} when reading scan results from {file_name}")
        print_status_msg(2)

def load_scan_results():
    """ Dialogue to load list of scan_results from a file """
    # List files with .ipfile - extension
    # Let user select
    # Read file
    misc_tools.clear_screen()
    set_status_msg("Select file to load scan results from")
    print_status_msg()
    selected_file = display_file_list(
                        extension=SCAN_RESULT_FILE_EXT,
                        selectable=True,
                        start_row=FILE_LIST_START_ROW,
                        start_col=FILE_LIST_START_COL)
    if not selected_file is None:
        load_scan_result_file(selected_file)

def clear_scan_results():
    """ Ersing results from variable """
    set_status_msg("Do you want to erase results from memory? (Y/N)")
    print_status_msg()
    if misc_tools.get_key() == "Y":
        _scan_results.clear()
        global _scan_saved
        _scan_saved = True
        set_status_msg("Results are erased!")
        print_status_msg(2)

# Constant with list of tuple containing:
# Selector, menu item and funcion to run
# Lines commented out are yet to be implemented
SCAN_RESULT_MENU_LIST = [
    ("1", "Show full results",display_scan_results),
    ("2", "Show stripped results",display_stripped_scan_results),
    ("3", "Save result to file", save_scan_results),
    ("4", "Load results scan from file", load_scan_results),
    ("9", "Clear scan results", clear_scan_results),
    ("0", "Return to main menu", misc_tools.nothing),
    ("Q", "Quit program", end_program)
]

def scan_results_menu():
    """ Display Scan result menu to show, save and reload scan results """
    selection = ""
    while selection != "0":
        misc_tools.clear_screen()
        set_status_msg("Waiting for input. Select from Scan results menu")
        print_status_msg()
        print(MENU_COLOR)
        selection = misc_tools.menu(
            SCAN_RESULT_MENU_LIST,
            5,
            MENU_WIDTH-6,
            MENU_START_ROW,
            MENU_START_COL,
            menu_header="Scan results menu")
        print(Fore.RESET)

# Constant with list of tuple containing:
# Selector, menu item and funcion to run
# Lines commented out are yet to be implemented
MAIN_MENU_LIST = [
        ("1", "IP address(es)...", ip_address_menu),
        ("2", "Arguments and flags...", args_menu),
        ("3", "Scan", scan),
        ("4", "Scan results...", scan_results_menu),
        # ("7", "Help",display_help),
        ("Q", "Quit program", misc_tools.nothing),
        # ("R", "Refresh screen", misc_tools.clear_screen),
    ]

def main_menu():
    """  Print main menu and handle response """
    set_status_msg("Waiting for input. Select from main menu.")
    print_status_msg()
    # print menu and wait for user selection
    print(MENU_COLOR)
    result = misc_tools.menu(
        MAIN_MENU_LIST,
        5,
        MENU_WIDTH-6,
        MENU_START_ROW,
        MENU_START_COL,
        menu_header="Laboration 1 by SweJob")
    print(Fore.RESET)
    return result

def main():
    """ Laboration 1 """
    menu_selection = ""
    while menu_selection != "Q":
        check_terminal_size()
        misc_tools.clear_screen()
        set_status_msg("Waiting for input. Select from main menu.")
        print_status_msg()
        menu_selection = main_menu()
    end_program()

if __name__ == "__main__":
    main()
