import ipaddress
import nmap
import misc_tools
import sys
import getopt

# Check if running on windows, otherwise assume linux
WINDOWS = misc_tools.is_windows()

# get a list of command line arguments
no_of_arguments = len(sys.argv)

# compare arguments with list of valid arguments


╠
   