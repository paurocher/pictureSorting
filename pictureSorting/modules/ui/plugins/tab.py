"""Neutral tab.
With info about version, available functions, a kind of bg image, ..."""
from pathlib import Path
from pprint import pprint as pp
import shutil

from Qt.QtWidgets import (
    QPushButton,
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QSplitter,
    QLayout,
)
from Qt.QtCore import (
    Qt,
)

from ..widgets.terminal import Terminal


class Tab(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.action_name = ""
        self.about_label = QLabel()
        self.about_text = ""

        self.layout = QVBoxLayout()
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.setLayout(self.layout)

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.splitter)

        self.top_widget = QWidget()
        self.top_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.top_layout = QVBoxLayout(self.top_widget)
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.bottom_widget = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_widget)

        self.splitter.addWidget(self.top_widget)
        # self.splitter.addWidget(self.bottom_widget)

        # I am executing this one in each tab after setting the about_text
        #  parameter (because I want to execute super first inside __init__
        #  because of aestethics of code?)
        #  I could run this from here, but I would have to move the about_text
        #  parameter of each tab before the super call.
        # self.build_top_ui()
        # self.build_bottom_ui()

    @property
    def about_text(self):
        return self._about_text

    @about_text.setter
    def about_text(self, text):
        self._about_text = text

    def build_title_ui(self) -> None:
        """Title and about label."""
        text_widget = QWidget()
        text_layout = QVBoxLayout()
        text_widget.setLayout(text_layout)
        text_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.about_label.setText(self.about_text)
        self.about_label.setMinimumHeight(10)
        self.about_label.setWordWrap(True)
        self.about_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        text_layout.addWidget(self.about_label)

        # self.layout.addStretch()
        # self.layout.addLayout(text_layout)

        # separator = QFrame(self)
        # separator.setFrameShape(QFrame.Shape.HLine)
        # separator.setFrameShadow(QFrame.Shadow.Sunken)
        # text_layout.addWidget(separator)

        self.top_layout.addWidget(text_widget)

    def build_main_ui(self):
        """The main ui for the tab."""
        pass

    def build_execute_ui(self) -> None:
        """The 'execute' side of things.

        Mainly the 'dry-run' and 'run' checkboxes.
        """
        self.top_layout.addStretch()

        bottom = QWidget()
        bottom_layout = QHBoxLayout()
        # bottom_layout.addStretch()
        # self.layout.addLayout(bottom_layout)
        bottom.setLayout(bottom_layout)

        self.recursive_checkbox = QCheckBox("Recursive")
        self.recursive_checkbox.setToolTip(
            "Scan all subfolders recursively."
        )
        self.recursive_checkbox.setCheckState(Qt.CheckState.Checked)
        bottom_layout.addWidget(self.recursive_checkbox)

        self.dry_run_checkbox = QCheckBox("Dry Run")
        self.dry_run_checkbox.setToolTip(
            "Do not process files, just print what would be processed."
        )
        self.dry_run_checkbox.setCheckState(Qt.CheckState.Checked)
        bottom_layout.addWidget(self.dry_run_checkbox)

        self.run_button = QPushButton("Run")
        self.run_button.setToolTip(
            "Start the process."
        )
        self.run_button.clicked.connect(self.run)
        bottom_layout.addWidget(self.run_button)

        # separator = QFrame(self)
        # separator.setFrameShape(QFrame.Shape.HLine)
        # separator.setFrameShadow(QFrame.Shadow.Sunken)
        # self.layout.addWidget(separator)

        self.top_layout.addWidget(bottom)

    def build_terminal_ui(self):
        self.terminal = Terminal(self)
        # self.bottom_layout.addWidget(self.terminal)
        self.splitter.addWidget(self.terminal)


    def run(self):
        """Run the command of this tab."""
        pass


    def move(self, src_path: Path, dest_path: Path):
        """Move a path to another destination.

        Args:
            src_path (Path): The source path.
            dest_path (Path): The destination path.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if dest_path.exists():
            self.terminal.error(
                f"Failed to move {src_path} to {dest_path}"
            )
            return False
        shutil.move(src_path, dest_path)
        return True

    def open_file_browser(self, target_field: str) -> None:
        # TODO: if target field already has a path, make the file dialog open up
        #  in that path.
        target = Path().home()
        if target_field.text():
            target = str(Path(target_field.text()).absolute())
        print("Target", target)
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        file_dialog.setDirectory(target) # Does not work!!! :(

        # selected_dir = QFileDialog.getExistingDirectory(None, target)

        selected_dir = file_dialog.getExistingDirectory(
            caption="Select a folder"
        )
        target_field.setText(selected_dir)