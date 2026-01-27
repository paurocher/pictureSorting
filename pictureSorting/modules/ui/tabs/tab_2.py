from .tab import Tab

class Tab2(Tab):
    def __init__(self):
        super().__init__()
        self.about_text = ("Convert HEIF to JPG")
        self.build_ui()

