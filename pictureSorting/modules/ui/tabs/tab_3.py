
from .tab import Tab

class Tab3(Tab):
    def __init__(self):
        super().__init__()
        self.about_text = (
            "Find and move hidden files (starting with a dot) to the trash or "
            "a specific folder.")
        self.build_ui()

