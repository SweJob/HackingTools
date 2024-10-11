from swejob_tools import misc_tools

def test_get_key():
    """
    Testing the get_key(function) in misc_tools
    Is behaviour good on all os?
    """
    while True:
        key_pressed = misc_tools.get_key(mode=1,catch_break=False)
        print(key_pressed)
        if key_pressed == "Q":
            break
def test_resize_terminal():
    print(f"Rows: {misc_tools.get_terminal_height()}")
    print(f"Columns: {misc_tools.get_terminal_width()}")
    misc_tools.resize_term(40,100)
    print(f"Rows: {misc_tools.get_terminal_height()}")
    print(f"Columns: {misc_tools.get_terminal_width()}")
    input("Press enter to continue")
    
def main():
    """
    uncomment  the various functions to test their behaviour
    """
    # test_get_key()
    
    test_resize_terminal()
    
if __name__ == "__main__":
    main()
    
