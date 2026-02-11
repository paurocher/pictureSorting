"""Move / delete hidden files."""
from functools import lru_cache
import os
from pathlib import Path
from Qt.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QLineEdit,
    QFileDialog
)
from Qt.QtCore import (
    Qt,
)
from shutil import move
from typing import Tuple, Any, Dict

from ... import utilities
from .tab import Tab

class Tab03(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.about_text = (
            "Find and move hidden files (starting with a dot) to the trash or "
            "a specific folder.\n"
            "Note that folders will be kept untouched, even if their name "
            "starts with a dot."
        )
        self.action_name = "Move hidden files"

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()


        self.src_field.setText("/home/fuku/Desktop/test")
        self.dst_field.setText("/home/fuku/Desktop/test_trash")

    def build_main_ui(self):
        top_ui = QWidget()
        file_browserlayout = QGridLayout()
        file_browserlayout.setColumnStretch(1, 1)
        top_ui.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # self.layout.addLayout(file_browserlayout)
        top_ui.setLayout(file_browserlayout)

        self.src_label = QLabel("Source folder: ")
        file_browserlayout.addWidget(self.src_label, 0, 0)

        self.src_field = QLineEdit()
        file_browserlayout.addWidget(self.src_field, 0, 1)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.open_file_browser(self.src_field))
        file_browserlayout.addWidget(browse_button, 0, 2)
        
        self.dst_label = QLabel("Destination folder: ")
        file_browserlayout.addWidget(self.dst_label, 1, 0)

        self.dst_field = QLineEdit()
        file_browserlayout.addWidget(self.dst_field, 1, 1)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.open_file_browser(self.dst_field))
        file_browserlayout.addWidget(browse_button, 1, 2)

        self.top_layout.addWidget(top_ui)

    def open_file_browser(self, target_field):
        file_dialog = QFileDialog()
        # file_dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        selected_dir = file_dialog.getExistingDirectory(
            caption="Select a folder"
        )
        target_field.setText(selected_dir)

    # @lru_cache(maxsize=10)
    def run(self):
        """Move hidden files."""
        paths_check, messages, src_path, dst_path = self.check_paths()
        if not paths_check:
            self.terminal.append(messages)
            return

        paths = utilities.scan_dir(
            src_path, recursive=self.recursive_checkbox.isChecked()
        )
        # print(paths)

        hidden_paths = utilities.find_hidden(paths)
        if not hidden_paths:
            self.terminal.append("No hidden files found.")
            return

        hidden_paths = self.rename_duplicates(hidden_paths)

        sizes = sorted([size["size"] for name, size in hidden_paths.items()])

        stats = [
            f"\nTotal hidden files found: {len(hidden_paths)}",
            f"Smallest: {min(sizes)}Mb, Largest: {max(sizes)}Mb",
            f"\n{'-' * 20}\n"
        ]
        self.terminal.append("\n".join(stats))

        if self.dry_run_checkbox.checkState() == Qt.CheckState.Checked:
            return

        for path, details in hidden_paths.items():
            if details["rename"]:
                new_path = Path().joinpath(dst_path, details["rename"])
                move(path, new_path)
            else:
                new_path = Path().joinpath(dst_path, path.name)
                move(path, new_path)
        self.terminal.append("Moved files to destination folder.")

    def rename_duplicates(self, paths: Dict[Any, Dict[str, Any]]):
        """Rename duplicate hidden files.
        
        Args:
            paths (dict): hidden files paths and details

        Returns:
            dict: Path {"size": float, "rename": str}

        """
        # TODO: move this method to utilities and make it work for all cases
        file_names = []
        for path, details in paths.items():
            details["rename"] = None
            stem = path.stem
            if stem in file_names:
                count = len([s for s in file_names if s.startswith(stem)])
                stem = stem + ("_BIS_" * count)
                details["rename"] = stem
            new_path = Path().joinpath(path.parent, stem)
            file_names.append(stem)
            self.terminal.append(f"{path} --> {new_path}")
        return paths

    def check_paths(self) -> Tuple[bool, str, Path, Path]:
        """Make sure paths fields are not empty and are existing paths.

        Returns:
            tuple:
                bool: whether all checks passed
                str: the messages to print to the terminal
                Path: src path
                Path: dst path

        """
        checks_passed = True
        message = []

        src_path = self.src_field.text()
        dst_path = self.dst_field.text()
        if not src_path:
            message.append("Source path mut not be empty.")
            checks_passed = False
        if not dst_path:
            message.append("Destination path mut not be empty.")
            checks_passed = False

        src_path = Path(src_path)
        dst_path = Path(dst_path)
        if not src_path.exists():
            message.append("Source path does not exist.")
            checks_passed = False
        if not src_path.is_dir():
            message.append("Source path is not a directory.")
            checks_passed = False
        if not dst_path.exists():
            message.append("Destination path does not exist.")
            checks_passed = False
        if not dst_path.is_dir():
            message.append("Destination path is not a directory.")
            checks_passed = False

        return checks_passed, "\n".join(message), src_path, dst_path