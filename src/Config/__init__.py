from src.Config.user_data import *
from src.Config.pages import *  
import os

BROWSER_ENABLED=True if os.getenv("BROWSER_ENABLED", False) == "True" else False