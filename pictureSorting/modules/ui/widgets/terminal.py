"""Terminal output."""

from Qt.QtWidgets import QTextEdit


class Terminal(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setReadOnly(True)

    def error(self, text: str) -> None:
        prefix = "<span style='color: #333333; background-color: #DB0B0B;'><b>"
        self.append(f"{prefix}{text}")

    def info(self, text: str) -> None:
        prefix = ""
        self.append(f"{prefix}{text}")

    def success(self, text: str) -> None:
        prefix = "<span style='color: #AAAAAA; background-color: #099400;'><b>"
        self.append(f"{prefix}{text}")

    def warning(self, text: str) -> None:
        prefix = "<span style='color: #555555; background-color: #FCC500;'><b>"
        self.append(f"{prefix}{text}")