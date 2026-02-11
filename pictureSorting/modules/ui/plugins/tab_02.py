"""Convert HEIF to JPG."""
from .tab import Tab

class Tab02(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.about_text = "Convert HEIF to JPG"

        self.action_name = "Convert HEIF to JPG"

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()