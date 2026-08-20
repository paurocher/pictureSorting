"""Picture Sorting tab."""
import copy
from datetime import date
from pathlib import Path
from pprint import pprint as pp

from Qt.QtWidgets import (
    QAction,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from Qt.QtCore import (
    Qt,
)

from ... import globals as glb
from ... import utilities as utils
from .tab import Tab

class Tab01(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.action_name = "Sort Media"
        self.about_text = (
            "Sort pictures or videos by date and move them into a year / month "
            "/ day folder structure in the selected destination folder."
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

        self.mode = QPushButton("Media Type", self)
        mode_menu = QMenu(self.mode)
        pic_action = QAction("Pictures", self.mode)
        pic_action.triggered.connect(lambda: self.generic_action_do("Pictures"))
        mode_menu.addAction(pic_action)
        mov_action = QAction("Videos", self.mode)
        mov_action.triggered.connect(lambda: self.generic_action_do("Videos"))
        mode_menu.addAction(mov_action)
        self.mode.setMenu(mode_menu)
        file_browserlayout.addWidget(self.mode, 0, 0)

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
        """Sort pictures.

        Move image and movie files to appropriate location based on the date.
        Append _BIS_ to duplicate file names to avoid conflicts or overwriting.
        !!DO NOT RUN THIS FROM ALREADY ORGANIZED BY DATE FOLDERS. OTHERWISE, ALL
        FILES WILL HAVE __BIS__ APPENDED TO THEIR NAME!!!"""

        if self.mode.text() not in  ["Pictures", "Videos"]:
            self.terminal.warning(
                "Please select a media type to process."
            )
            return False

        src_check, messages, src_path = self.check_paths(self.src_field, "Source Field")
        self.terminal.error(messages)
        dst_check, messages, self.dest_dir = self.check_paths(self.dst_field, "Destination Field")
        self.terminal.error(messages)
        if not any([src_check, dst_check]):
            return False

        self.src_dir_files = self.scan_dir(
            src_path, recursive=self.recursive_checkbox.isChecked()
        )

        # filter by extension
        file_filter = glb.IMAGE_FORMATS
        if self.mode.text() == "Videos":
            file_filter = glb.VIDEO_FORMATS
        self.src_dir_files = utils.filter_by_extension(
            self.src_dir_files, file_filter
        )

        sizes = sorted([size["size"] for name, size in self.src_dir_files.items()])
        stats = [
            f"\nTotal files found: {len(self.src_dir_files)}",
            f"Smallest: {min(sizes)}Mb, Largest: {max(sizes)}Mb",
            f"\n{'-' * 20}\n"
        ]
        self.terminal.info("\n".join(stats))

        # Get all the paths that exist in the dst folder structure. Later we
        #  will compare to the new paths to check for duplicates
        self.get_all_dst_dir_paths()
        # self.clean_dst_files()

        for file, details in self.src_dir_files.items():
            # find file dates out
            details["dates"] = utils.get_file_dates(file, self.mode.text().lower())
            details["dates"]["smaller_date"] = utils.get_earlier_date(details["dates"])

            # Create the dir structures based on the smaller date (non-destructive)
            root_path = self.build_date_dir(details["dates"]["smaller_date"])

            # Build temp destination paths
            details["temp_dest_path"] = root_path / file.parts[-1]

            # Rename duplicates
            self.rename_duplicates(details)

            self.terminal.info(f"{file} --> {details['final_dest_path']}")

            if not self.dry_run_checkbox.checkState() == Qt.CheckState.Checked:
                # Move files
                self.move(file, details["final_dest_path"])
        # pp(self.src_dir_files)


        self.terminal.info(f"\n{'- ' * 40}\n")

    def build_date_dir(self, date: date):
        """Build a destination folder path based on a date.

        Args:
            date (date)

        Returns: Path
        """
        year = str(date.year)
        month = "{:0>2}".format(date.month)
        day = "{:0>2}".format(date.day)
        path = self.dest_dir.joinpath(year, month, day)
        # print(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def generic_action_do(self, text: str) -> None:
        self.mode.setText(text)
