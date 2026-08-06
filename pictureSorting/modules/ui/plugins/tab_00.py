"""Neutral tab.
With info about version, available functions, a kind of bg image, ..."""
from Qt.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QLabel,
    QLayout,
    QPushButton,
    QMenuBar,
    QMenu,
    QAction,
    QTabWidget,
    QStackedWidget,
    QSizePolicy,
)
from Qt.QtCore import (
    QSize,
    Qt,
)
from Qt.QtGui import (
    QPixmap,
    QPainter
)
from .tab import Tab

class Tab00(Tab):
    def __init__(self, parent, previous_tab):
        super().__init__(parent)

        self.previous_tab = previous_tab
        self.action_name = "Picture Operations"
        self.build_ui()

    def build_ui(self):
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        text_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        title = QLabel(f"{self.action_name}\n")
        title.setStyleSheet("font-size: 20px; font-weight: bold")
        # title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

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

        self.layout.addLayout(text_layout)
        self.layout.addStretch()

    def mouseReleaseEvent(self, event):
        self.parent.tabs.setCurrentIndex(self.previous_tab)

# TODO: show this tab at the bgining and from menuBar/.../About