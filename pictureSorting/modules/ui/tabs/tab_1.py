"""Picture Sorting tab."""
from .tab import Tab

class Tab1(Tab):
    def __init__(self):
        super().__init__()
        self.about_text = ("Sort Pictures")
        self.build_ui()

