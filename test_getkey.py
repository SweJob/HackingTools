from swejob_tools import misc_tools

a = misc_tools.get_key(test=True)
while a != "Q":
    print(a)    
    a = misc_tools.get_key(test=True)
