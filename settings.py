# settings.py
# Constants module

"""Module for app constants as database name and images path"""

import os
import sys

# Database file name
DATABASE = 'sqlite:///contacts.db'

# Images path
platform = sys.platform

IMG_PATH = os.getcwd() + "//images//" if "linux" in platform.lower() \
        else os.getcwd() + "\\images\\"

# Widgets Colors
FRAME_BG = "#FBFBEF"
BTN_ACTIVE_BG = "#F79F81"
BTN_BG = "#F8ECE0"
