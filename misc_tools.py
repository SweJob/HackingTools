import platform

def is_windows():
    if platform.system().lower() == "windows":
        return True
    else:
        return False