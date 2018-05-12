from .Sdk import Sdk

# Import GUI if Win
import sys
if sys.platform.lower().startswith("win"):
    from .gui import SdkGui
