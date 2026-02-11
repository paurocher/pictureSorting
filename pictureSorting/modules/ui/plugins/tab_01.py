"""Picture Sorting tab."""
from .tab import Tab

class Tab01(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.about_text = "Sort Pictures"
        self.action_name = "Sort Pictures"

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()
