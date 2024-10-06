import platform

def is_windows():
    if platform.system().lower() == "windows":
        return True
    else:
        return False
    
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def menu(menu_header:str, menu_items, selector_width:int, text_width:int):
    # Show a menu, accept input, run a method (is this possible?)
    # menu items should be a list containing a tuple (?) : character to select, text to display, function to execute
    selectors = list()
    functions = list()
    
    # Create strings for frame around header
    header_top_line =  "╔" + "═"*(selector_width +text_width + 1) + "╗"
    header_bottom_line = "╠"+ "═"*selector_width + "╦" + "═"*text_width + "╣"
    
    # create string for  frame around menu
    # top_line = "╔" + "="*selector_width + "╦" + "═"*text_width + "╗"
    # separator_line = "╠" + "="*selector_width + "╬" + "═"*text_width + "╣"
    bottom_line = "╠"+ "═"*selector_width + "╩" + "═"*text_width + "╣"
    
    # Create strings for selction statement
    selection_bottom_line =  "╚" + "═"*(selector_width +text_width + 1) + "╝"
    
    # print menu header with frame
    print(header_top_line)
    print("║"+ menu_header.center(selector_width + text_width + 1) + "║")
    print(header_bottom_line)
    
    # print menu items with frame
    for menu_item in menu_items:
        selector = menu_item[0]
        
        # add selector to valid_selector list
        selectors.append(selector)
        
        # add function to function_list
        function = menu_item[2]
        functions.append(function)
        
        menu_text = menu_item[1]
        print("║ "+ selector.ljust(selector_width-2) + " ║ " + menu_text.ljust(text_width-1) + "║")
    
    
    print(bottom_line)
    print("║"+ "Select".ljust(selector_width + text_width + 1) + "║")
    print(selection_bottom_line)
    
    
    # Get the selection
    selection = input("")
    if selection in selectors:
        #execute function
        selected_function = functions[selectors.index(selection)]
        selected_function()
        
    else:
        input(f"{selection} is not a valid option, press enter to try again")
        

def test_function1():
    print (f"test_function1 was run")

def test_function2():
    print (f"test_function2 was run")
    
def test_function3():
    print (f"test_function3 was run")
    
def main():
    
    while True:
        menu_items =[
            ("1","Testar 1",test_function1),
            ("2","Testar 2",test_function2),
            ("3","Testar 3",test_function3),
            ("4","Quit", quit)
        ]
    
        menu("Testmenu",menu_items,4, 15)
    

if __name__ == "__main__":
    main()