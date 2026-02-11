from pathlib import Path
from Qt.QtWidgets import (
    QMainWindow,
    QApplication,
    QFrame,
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
    QSplitter,
)
from Qt.QtCore import (
    QSize,
    Qt,
)

from ...media import sources
from .widgets.mode_menu import ModeMenu
from .widgets.terminal import Terminal
from . import plugins
from .plugins.tab_00 import Tab00


# import stylesheet
this_path = Path(__file__)
stylesheet = Path().joinpath(this_path.parent, "stylesheet.qss")



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setStyleSheet(stylesheet.read_text())

        self.setWindowTitle("Picture Sorter")
        self.setMinimumSize(QSize(640, 480))

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        # self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(5, 10, 5, 10)
        self.setCentralWidget(self.central_widget)

        # this one mainy helps us keep track of what was the satus before we
        #  switch to 'help' so we can go back to it when we click on the
        #  help panel
        self.current_tab_index = 0

        self.create_top_ui()

        self.create_tabs()

        self.create_menu_actions()
        self.create_menubar()


    def create_menu_actions(self):
        """Create the actions for the menu bar.

        These are static, application-wide.
        """
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.quit_app)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about_tab)

        self.helper_action = QAction("Helper", self)
        self.helper_action.setShortcut("Ctrl+Z")
        self.helper_action.triggered.connect(self.helper)

        self.terminal_show_action = QAction("Show Terminal", self)
        self.terminal_hide_action = QAction("Hide Terminal", self)
        self.terminal_clear_action = QAction("Clear Current Terminal", self)
        self.terminal_clear_action.setShortcut("Ctrl+Shift+G")
        self.terminal_clear_action.triggered.connect(self.terminal_clear)
        self.terminal_bottom_action = QAction("Terminal to Bottom", self)
        self.terminal_right_action = QAction("Terminal to Right", self)

    def helper(self):
        """Function to test shit.

        Change the code here as you please to test it with the 'helper'
        action or Ctrl+Z"""
        print(plugins.plugin_getter.discovered_plugins)

    def create_menubar(self):
        """Create the application menubar."""
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = QMenu("&File", self)
        menubar.addMenu(file_menu)
        file_menu.addAction(self.quit_action)

        help_menu = QMenu("&Help", self)
        menubar.addMenu(help_menu)
        help_menu.addAction(self.about_action)
        help_menu.addAction(self.helper_action)

        terminal_menu = QMenu("&Terminal", self)
        menubar.addMenu(terminal_menu)
        terminal_menu.addAction(self.terminal_show_action)
        terminal_menu.addAction(self.terminal_hide_action)
        terminal_menu.addAction(self.terminal_clear_action)
        terminal_menu.addAction(self.terminal_bottom_action)
        terminal_menu.addAction(self.terminal_right_action)

    def create_top_ui(self):
        """Create the topmost ui in the window.

        Just the 'mode' pulldown menu for now."""
        title = QLabel("Mode: ")
        self.mode_menu = ModeMenu(self)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)
        layout.addWidget(self.mode_menu)
        self.central_layout.addLayout(layout)
        # self.central_layout.addWidget(title)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        # self.central_layout.addWidget(separator)

    def create_tabs(self):
        """Create the containing tabs for each functionality."""
        self.tabs = QStackedWidget()
        self.tabs.setMinimumHeight(50)
        self.tabs.insertWidget(0, Tab00(self, 0))
        for i, (tab_name, object) in enumerate(plugins.plugin_getter.discovered_plugins.items()):
            i = i + 1
            object = object(self)
            self.tabs.insertWidget(i, object)
            self.mode_menu.add_action(i, object.action_name)
        # self.splitter.addWidget(self.tabs)
        self.central_layout.addWidget(self.tabs)

    # def create_terminal(self):
    #     self.terminal = Terminal(self)

    def terminal_clear(self):
        self.tabs.widget(self.current_tab_index).terminal.clear()

    def show_about_tab(self):
        self.tabs.widget(0).previous_tab = self.current_tab_index
        self.tabs.setCurrentIndex(0)

    def keyPressEvent(self, event):
        key = event.text()
        if key in [str(i) for i in range(1, 10)]:
            key = int(key)
            if key < self.tabs.count():
                self.current_tab_index = key
                self.mode_menu.setText(
                    self.mode_menu.menu.actions()[key - 1].text()
                )
                self.tabs.setCurrentIndex(key)


    def quit_app(self):
        self.close()


def run():
        app = QApplication([])
        a = MainWindow()
        a.show()
        app.exec()
