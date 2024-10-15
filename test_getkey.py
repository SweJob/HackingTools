from swejob_tools import misc_tools

a = misc_tools.get_key(mode=9)
while a != "Q":
    print(a)    
    a = misc_tools.get_key(mode=9)
