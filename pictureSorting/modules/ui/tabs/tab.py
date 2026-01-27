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

class Tab(QWidget):
    def __init__(self):
        super().__init__()

        self.about_label = QLabel()
        self.about_text = ""

    @property
    def about_text(self):
        return self._about_text

    @about_text.setter
    def about_text(self, text):
        self._about_text = text

    def build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.about_label.setText(self.about_text)
        text_layout.addWidget(self.about_label)

        layout.addLayout(text_layout)
        layout.addStretch()