"""Terminal output."""

from Qt.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMenuBar,
    QMenu,
    QAction,
    QTabWidget,
    QStackedWidget,
    QLineEdit,
    QTextEdit,
)
from Qt.QtCore import (
    QSize,
    Qt,
)


class Terminal(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setReadOnly(True)

