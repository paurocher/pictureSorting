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
        self.menu_actions = {}

        self.setMinimumWidth(200)

        self.menu = QMenu(self)
        self.setMenu(self.menu)

    def add_action(self, index: int, name: str) -> None:
        """Create a new action and add it to the actions dict."""
        action = QAction(name, self)
        action.triggered.connect(lambda: self.generic_action_do(index, name))
        self.menu_actions[name] = action
        self.menu.addAction(action)

    def generic_action_do(self, index:int, text: str) -> None:
        self.setText(text)
        self.parent.tabs.setCurrentIndex(index)
        self.parent.current_tab_index = index
