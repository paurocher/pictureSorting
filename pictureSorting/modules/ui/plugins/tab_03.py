"""Move hidden files.

This moves all files into one single dir.
This will not build the year/month/day dir structure.
"""
from Qt.QtWidgets import (
    QWidget,
    QCheckBox,
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
from typing import Tuple, Any, Dict

from ... import utilities as utils
from .tab import Tab
from ... import globals as glb

class Tab03(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.action_name = "03 Move hidden files"
        self.about_text = (
            "Find and move hidden files (starting with a dot) to the trash or "
            "a specific folder.\n"
            "Note that folders will be kept untouched, even if their name "
            "starts with a dot."
        )

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()

        self.src_field.setText("/home/fuku/Desktop/test")
        self.dst_field.setText("/home/fuku/Desktop/test_pic_trash")

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

    def run(self):
        """Move hidden files."""
        src_check, messages, src_path = utils.check_paths(self.src_field, "Source Field")
        self.terminal.error(messages)
        dst_check, messages, glb.DEST_DIR = utils.check_paths(self.dst_field, "Destination Field")
        self.terminal.error(messages)

        if not all([src_check, dst_check]):
            return

        glb.SRC_DIR_FILES = utils.scan_dir(
            src_path, recursive=self.recursive_checkbox.isChecked()
        )

        # Build temp destination paths
        utils.get_all_dst_dir_paths()
        utils.clean_dst_files()
        utils.build_temp_dst_paths()

        glb.SRC_DIR_FILES = utils.find_hidden()
        if not glb.SRC_DIR_FILES:
            self.terminal.info("No hidden files found.")
            return

        utils.rename_duplicates()

        for path, details in glb.SRC_DIR_FILES.items():
            self.terminal.info(f"{path} --> {details['final_dest_path']}")

        sizes = sorted([size["size"] for name, size in glb.SRC_DIR_FILES.items()])

        stats = [
            f"\nTotal hidden files found: {len(glb.SRC_DIR_FILES)}",
            f"Smallest: {min(sizes)}Mb, Largest: {max(sizes)}Mb",
            f"\n{'-' * 20}\n"
        ]
        self.terminal.info("\n".join(stats))

        if self.dry_run_checkbox.checkState() == Qt.CheckState.Checked:
            return

        for path, details in glb.SRC_DIR_FILES.items():
            self.move(path, details["final_dest_path"])

        self.terminal.info("Done.")

