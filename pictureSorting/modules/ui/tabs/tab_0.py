"""Neutral tab.
With info about version, available functions, a kind of bg image, ..."""
from PyQt5.QtGui import QPixmap
from Qt.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QLabel,
    QPushButton,
    QMenuBar,
    QMenu,
    QAction,
    QTabWidget,
    QStackedWidget,
)
from Qt.QtCore import (
    QSize,
    Qt,
)
from Qt.QtGui import (
    QPixmap,
    QPainter
)

class Tab0(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        title = QLabel("Picture Operations\n")
        title.setStyleSheet("font-size: 20px; font-weight: bold")

        about = QLabel(
            "Little tool to organize pictures and movies based on their "
            "creation date.\n"
            "\n"
            "Offers a few more tools to:\n"
            "   - split folders into a specified amount of files\n"
            "   - delete hidden files\n"
            "   - delete files by extension\n"
            "   - delete files by file size\n"
        )

        text_layout.addWidget(title)
        text_layout.addWidget(about)

        layout.addLayout(text_layout)
        layout.addStretch()


