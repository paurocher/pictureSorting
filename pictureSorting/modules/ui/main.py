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
    QStackedWidget
)
from Qt.QtCore import (
    QSize,
    Qt,
)

from widgets.mode_menu import ModeMenu
from tabs.tab_0 import Tab0
from tabs.tab_1 import Tab1
from tabs.tab_2 import Tab2
from tabs.tab_3 import Tab3

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Picture Sorter")
        self.setMinimumSize(QSize(640, 480))

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setCentralWidget(self.central_widget)

        self.create_actions()
        self.create_menu()
        self.create_top_ui()
        self.create_tabs()

    def create_actions(self):
        """Create the actions for the menu bar."""
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.quit_app)

        self.help_action = QAction("Help", self)

    def create_menu(self):
        """Create the application menu."""
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = QMenu("&File", self)
        menubar.addMenu(file_menu)
        file_menu.addAction(self.quit_action)

        help_menu = QMenu("&Help", self)
        menubar.addMenu(help_menu)
        help_menu.addAction(self.help_action)

    def create_top_ui(self):
        """Create the topmost ui in the window."""
        title = QLabel("Mode: ")
        self.mode = ModeMenu(self)
        # self.mode.action_a.triggered.connect(self.mode_menu_action_a)
        # self.mode.action_b.triggered.connect(self.mode_menu_action_b)
        # self.mode.action_c.triggered.connect(self.mode_menu_action_c)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)
        layout.addWidget(self.mode)
        self.central_layout.addLayout(layout)
        # self.central_layout.addWidget(title)


    def create_tabs(self):
        """Create the containing tabs for each functionality."""
        self.tabs = QStackedWidget()
        tab0 = Tab0()
        tab1 = Tab1()
        tab2 = Tab2()
        tab3 = Tab3()
        self.tabs.resize(300,200)

        self.tabs.insertWidget(0, tab0)
        self.tabs.insertWidget(1, tab1)
        self.tabs.insertWidget(2, tab2)
        self.tabs.insertWidget(3, tab3)

        self.central_layout.addWidget(self.tabs)

    # def mode_menu_action_a(self):
    #     self.tabs.setCurrentIndex(0)
    #
    # def mode_menu_action_b(self):
    #     self.tabs.setCurrentIndex(1)
    #
    # def mode_menu_action_c(self):
    #     self.tabs.setCurrentIndex(2)

    def quit_app(self):
        self.close()

app = QApplication([])
a = MainWindow()
a.show()
app.exec()
