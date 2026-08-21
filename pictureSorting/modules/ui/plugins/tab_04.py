"""Move / files if they match a specific extension.

This moves all files into one single dir.
This will not build the year/month/day dir structure.
"""

from functools import lru_cache
import os
from pathlib import Path
from pprint import pprint as pp

from Qt.QtWidgets import (
    QCheckBox,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QLineEdit,
    QFileDialog,
)
from Qt.QtGui import (
    QRegExpValidator
)
from Qt.QtCore import (
    Qt,
    QRegExp,
)

import re
from typing import Tuple, Any, Dict

from ... import utilities as utils
from ... import globals as glb
from .tab import Tab

class Tab04(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.action_name = "04 Move files by extension"
        self.about_text = (
            "Find and move files with a specific extension to a specific "
            "folder.\n"
            "Enter a comma separated list of extensions (e.g. jpg,png,mp4)"
        )

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

        extension_label = QLabel("Extension(s): ")
        file_browserlayout.addWidget(extension_label, 0, 0)

        self.extension_field = QLineEdit()
        input_validator = QRegExpValidator(
            QRegExp("[A-Za-z0-9,]+[A-Za-z0-9,.]+")
            # QRegExp("(?([*]+)|[A-Za-z0-9,]+[A-Za-z0-9,.]+)")
        )
        self.extension_field.setValidator(input_validator)
        file_browserlayout.addWidget(self.extension_field, 0, 1)
        self.extension_field.setText("exr,jpg,png")

        self.any_extension = QCheckBox("Any Extension")
        self.any_extension.clicked.connect(self.any_extension_check)
        file_browserlayout.addWidget(self.any_extension, 0, 2)

        self.src_label = QLabel("Source folder: ")
        file_browserlayout.addWidget(self.src_label, 1, 0)

        self.src_field = QLineEdit()
        file_browserlayout.addWidget(self.src_field, 1, 1)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.open_file_browser(self.src_field))
        file_browserlayout.addWidget(browse_button, 1, 2)

        self.dst_label = QLabel("Destination folder: ")
        file_browserlayout.addWidget(self.dst_label, 2, 0)

        self.dst_field = QLineEdit()
        file_browserlayout.addWidget(self.dst_field, 2, 1)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.open_file_browser(self.dst_field))
        file_browserlayout.addWidget(browse_button, 2, 2)

        self.top_layout.addWidget(top_ui)

    def run(self):
        """Move hidden files."""
        src_check, messages, src_path = self.check_paths(self.src_field, "Source Field")
        self.terminal.info(messages)
        dst_check, messages, self.dest_dir = self.check_paths(self.dst_field, "Destination Field")
        self.terminal.info(messages)
        if not any([src_check, dst_check]):
            return

        self.src_dir_files = self.scan_dir(
            src_path, recursive=self.recursive_checkbox.isChecked()
        )

        # Build temp destination paths
        self.get_all_dst_dir_paths()
        # self.clean_dst_files()
        self.build_temp_dst_paths()

        # Filter by extension
        if not self.any_extension.isChecked():
            self.src_dir_files = utils.filter_by_extension(
                self.src_dir_files,
                self.extension_field.text().split(",")
            )

        if not self.src_dir_files:
            return

        # pp(self.dest_dir_files)
        for src_path, details in self.src_dir_files.items():
            self.rename_duplicates(details)
            self.terminal.info(f"{src_path} --> {details['final_dest_path']}")

        sizes = sorted([size["size"] for name, size in self.src_dir_files.items()])
        stats = [
            f"\nTotal files found: {len(self.src_dir_files)}",
            f"Smallest: {min(sizes)}Mb, Largest: {max(sizes)}Mb",
            f"\n{'-' * 20}\n"
        ]
        self.terminal.info("\n".join(stats))

        if self.dry_run_checkbox.isChecked():
            return

        for path, details in self.src_dir_files.items():
            self.move(path, details["final_dest_path"])

        self.terminal.info("\nDone moving files.")

    def any_extension_check(self):
        """Execute when the 'any extension' checkbox is clicked."""
        if self.any_extension.isChecked():
            self.extension_field.setDisabled(True)
        else:
            self.extension_field.setEnabled(True)
