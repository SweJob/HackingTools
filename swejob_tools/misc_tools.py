""" 
Miscelaneous tools by SweJob:
is_windows() returns True if run on a windows system

is_float(string) returns True if provided string is represent a float-value

get_key() wait for any key to be pressed, return value of key

pos_print(row,column,text) prints text at the position [row,column]

menu(menu_items, selector_width, text_width, start_row , start_column, menu_header, select_prompt)
    prints a menu (selector and menu text)
    wait for a key to be pressed
    execute selected function

stop_program() stops execution of python-code

timer_decorator(func) decorator to measure executiontime of function

print_window(row_list, start_column, start_row, width, frame)
    prints text from row list from[start_row, start_column]
    if frame, width is the width of frame    
"""
import os
import platform
import sys
import time
import subprocess
from swejob_tools.getkey import getkey

def is_windows():
    """ Checks if program is running on a windows system """
    if platform.system().lower() == "windows":
        return True
    return False

if is_windows():
    import msvcrt
else:
    # what to import for reading key in linux??? to be implemented
    pass

def clear_screen():
    """
    clears terminal window on both windows and linux
    """
    if is_windows():
        os.system('cls')
    else:
        os.system('clear')

def is_float(string):
    """ Tests if the provided string is a float value """
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_key(mode=0, catch_break=True):
    """ 
    Grabs key pressed and returns key as a string
    If not alphabetical or numerical value, escape code is returned,
    ex: \t for tab, \r for return
    Ctrl-C is separatly handled and runs the stop_program() function,
    """
    if is_windows() or mode==0:
        key_pressed = ""
        # Grab a pressed key in windows environment
        if msvcrt.kbhit:
            key_val =  str(msvcrt.getch())
            #remove the "b'\" in the beginning of each string, and the trailing ' in the end
            key_pressed = key_val[2:].strip("'")
    elif mode == 1:
        # Grab a pressed key in linux environment
        # Not implemented yet
        key_pressed = getkey.getkey()

    elif mode == 2:
        pass


    # If catch_break is enabled and Ctrl-C is pressed, stop the program
    if catch_break and key_pressed == "\\x03":
        stop_program()
    return key_pressed

def get_terminal_width():
    """ 
    Returns width of terminal in columns
    """
    terminal_size=os.get_terminal_size()
    return terminal_size.columns

def get_terminal_height():
    """ 
    Returns height of terminal in lines
    """
    terminal_size=os.get_terminal_size()
    return terminal_size.lines

def resize_term(lines,columns):
    if is_windows():
        os.system(f"mode con: cols={columns} lines={lines}")
    else:
        print(f"\033[8;{lines};{columns}t", end="")

def pos_print(row=1,column=1,text=""):
    """ Prints text at [row,column] """
    print(f"\x1b[{row};{column}H{text}")

def menu(menu_items:list[tuple],
         selector_width:int,
         text_width:int,
         start_row=1,
         start_column=1,
         menu_header:str ="",
         select_prompt:str = ""):
    """
    Show a menu, accept input, run the selected method

    menu items should be a list containing a tuple:
    [("character to select", "text to display", function to execute)]
    example of menu_items:
    menu_items =[
        ("1","Testar 1",test_function1),
        ("2","Testar 2",test_function2),
        ("Q","Quit", stop_program
    ]
    Note that the function-part is the name of the function but no parenthesis "()" after.
    Thus no arguments can be passed to the function here.
    selector_width and text_width - column width for selectors and text respectively
    """
    selectors = []
    functions = []
    row = start_row
    column = start_column
    # Create strings for frame around header
    header_top_line =  "╔" + "═"*(selector_width +text_width + 1) + "╗"
    header_bottom_line = "╠"+ "═"*selector_width + "╦" + "═"*text_width + "╣"

    # create string for frame around menu
    no_header_top_line = "╔" + "═"*selector_width + "╦" + "═"*text_width + "╗"
    no_select_prompt_bottom_line = "╚"+ "═"*selector_width + "╩" + "═"*text_width + "╝"

    # Create strings for frame around selection prompt
    menu_bottom_line = "╠"+ "═"*selector_width + "╩" + "═"*text_width + "╣"
    select_prompt_bottom_line =  "╚" + "═"*(selector_width +text_width + 1) + "╝"

    # If header provided, print menu header with frame
    if len(menu_header) > 0:
        pos_print(row,column,header_top_line)
        row +=1
        pos_print(row,column,"║"+ menu_header.center(selector_width + text_width + 1) + "║")
        row +=1
        pos_print(row,column,header_bottom_line)
        row +=1
    # If no header, print topline with selctor column
    else:
        pos_print(row,column,no_header_top_line)
        row +=1

    # print menu items with frame
    for menu_item in menu_items:
        # selector is placed with 1 space from left frame, ends at least 1 space before divider
        # text start at 1 space from divider, ends at least 0 space to right frame
        menu_line = menu_item[0].ljust(selector_width-2)+" ║ "+ menu_item[1].ljust(text_width-1)
        pos_print(row,column,"║ " + menu_line +"║")
        row +=1
        # As we are looping through the menu list anyway, lets add selector to valid_selector list
        # valid_selector_list is used to verify input from user
        selectors.append(menu_item[0])
        # and add function to the list functions
        functions.append(menu_item[2])

    # If a select_prompt is provided, print it below the menu
    if len(select_prompt) > 0:
        pos_print(row,column,menu_bottom_line)
        row +=1
        pos_print(row,column,"║"+ "Select".ljust(selector_width + text_width + 1) + "║")
        row +=1
        pos_print(row,column,select_prompt_bottom_line)
        row +=1
    # If no select_prompt, print a bottomline
    else:
        pos_print(row,column,no_select_prompt_bottom_line)
        row +=1

    # Get the selection
    selection = get_key(1,True)

    # Compare with list of valid selectors
    if selection in selectors:
        # execute the correct function from functions
        functions[selectors.index(selection)]()
    else:
        pos_print(row,column, f"{selection} is not a valid option")
        input("Press Enter to continue")
        pos_print(row,column, " "*27)
        pos_print(row+1,column," "*27)

# function to stop program execution
def stop_program():
    """ Terminates running python code """
    sys.exit(0)

# Timer for functions
def timer_decorator(func):
    """ Decorator to get execution time of func """
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"The function was run in : {execution_time} sekunder")
        return result, execution_time
    return wrapper

# display a status window printed from a start row and column with a fixed width.
# each row is a tuple of strings that are concatenated to fit within the width of the status window
# frame is optional
def print_window(row_list:list, start_row=1, start_column=1, width=30, frame=True):
    """
    display a status window printed from a start row and column with a fixed width.
    each row is a tuple of strings that are concatenated 
    frame is optional. Text is then truncated to fit inside
    """
    row = start_row
    column = start_column
    if frame:
        # print top of frame
        pos_print(row,column,"╔" + "═"*(width-2) + "╗")
        row +=1
    # Loop through each row in row_list
    for row_tuple in row_list:
        row_string =""
        if frame:
            # add left border
            row_string = row_string +"║"
        # Loop through each part in each row_tuple
        for part in row_tuple:
            # adding each part of tuple as a string
            row_string = row_string + str(part)

        # If there is a frame, string needs to fit inside the frame before adding right "║"
        if frame:
            if len(row_string) > width-1:
                #shorten if to long
                row_string = row_string[:width-1]
            else:
                # add strailing spaces if to short
                row_string = row_string.ljust(width-1)
            row_string = row_string +"║"
        pos_print(row,column,row_string)
        row +=1
    # Print bottom of frame
    if frame:
        pos_print(row,column,"╚" + "═"*(width-2) + "╝")
        row +=1

def main():
    """ 
    main function used to test that functions behave as they are supposed to
    """
    menu_items =[
        ("1","Testar 1",print),
        ("2","Testar 2",pos_print),
        ("3","Testar 3",is_windows),
        ("Q","Quit", stop_program)
    ]
    resize_term(40,90)
    while True:
        os.system('cls')
        get_terminal_width()
        menu(menu_items,
            selector_width=4,
            text_width=15,
            start_row=2,
            start_column=1,
            menu_header="Testmenu")

if __name__ == "__main__":
    main()
