import json
import platform
import ctypes
import os

def get_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def write_config(options):
    d = get_config()
    with open('config.json', 'w') as f:
        json.dump({**d, **options}, f, indent=2, sort_keys=True)

def free_drive_space(as_string=False):
    """
    Checks and returns the remaining free drive space
    Parameters
    ----------
    as_string : bool, optional
        set to True if you want the function to return a formatted string.
        4278 -> 4.28 GB
    Returns
    -------
    space : float or str
        the remaining MB in float or as string if *as_string=True*
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('/'),
                                                   None, None,
                                                   ctypes.pointer(free_bytes))
        mb = free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs('/')
        mb = st.f_bavail * st.f_frsize / 1024 / 1024

    if as_string:
        if mb >= 1000:
            return '{:.2f} GB'.format(mb / 1000)
        else:
            return '{:.0f} MB'.format(mb)
    else:
        return mb