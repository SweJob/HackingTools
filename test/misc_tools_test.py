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
