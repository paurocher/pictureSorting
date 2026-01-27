from Qt.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMenu,
    QAction,
)
from Qt.QtCore import (
    QSize,
    Qt,
)


class ModeMenu(QPushButton):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setMinimumWidth(200)

        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.build_actions()

    def build_actions(self):
        action_a_name = "Sort Pictures"
        self.action_a = QAction(action_a_name, self)
        self.action_a.triggered.connect(lambda: self.action_a_do(action_a_name))
        self.menu.addAction(self.action_a)

        action_b_name = "Covert HEIF to JPG"
        self.action_b = QAction(action_b_name, self)
        self.action_b.triggered.connect(lambda: self.action_b_do(action_b_name))
        self.menu.addAction(self.action_b)

        action_c_name = "Remove hidden files"
        self.action_c = QAction(action_c_name, self)
        self.action_c.triggered.connect(lambda: self.action_c_do(action_c_name))
        self.menu.addAction(self.action_c)

    def action_a_do(self, text):
        self.setText(text)
        self.parent.tabs.setCurrentIndex(1)

    def action_b_do(self, text):
        self.setText(text)
        self.parent.tabs.setCurrentIndex(2)

    def action_c_do(self, text):
        self.setText(text)
        self.parent.tabs.setCurrentIndex(3)
