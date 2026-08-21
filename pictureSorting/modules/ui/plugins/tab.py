"""Neutral tab.
With info about version, available functions, a kind of bg image, ..."""
import copy
from pathlib import Path
from pprint import pprint as pp
import shutil
from typing import List, Dict, Any, Tuple

from Qt.QtWidgets import (
    QPushButton,
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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

        self.src_dir_files = None  # This will replace glb.SRC_DIR_FILES
        self.dest_dir = None  # This will replace glb.DEST_DIR
        self.dest_dir_files = None  # This will replace glb.DEST_DIR_FILES

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

    ###Non UI methods###

    def check_paths(
            self,
            field_obj: QLineEdit,
            field_name: str) -> Tuple[bool, str, Path]:
        """Make sure the UI path field is not empty and the path exists.

        If all is good: return True, no messages to print to terminal, and the
        string converted to a Path().
        If something is wrong: return false, message of what went wrong to print
        to terminal, and None.

        Args:
            field_obj ():
            field_name ():

        Returns:
            tuple:
                bool: whether all checks passed
                str: the messages to print to the terminal
                Path: src path
        """
        checks_passed = True
        message = []

        field_text = field_obj.text()

        if not field_text:
            message.append(f"{field_name} must not be empty.")
            checks_passed = False
            return checks_passed, "<br>".join(message), None
        path = Path(field_text)
        if not path.exists():
            message.append(f"{field_name} path does not exist.")
            checks_passed = False
            return checks_passed, "<br>".join(message), None
        if not path.is_dir():
            message.append(f"{field_name} path is not a directory.")
            checks_passed = False
            return checks_passed, "<br>".join(message), None

        return checks_passed, "<br>".join(message), path

    def build_temp_dst_paths(self) -> Path:
        """Build temp dst path.

        The resulting path has not been checked for duplicates."""
        for path, values in self.src_dir_files.items():
            values["temp_dest_path"] = self.dest_dir / path.parts[-1]

    def clean_dst_files(self):
        """Remove the _BIS_ from the dest paths.

        So each instance of a path counts as one when we rename the file
        paths to move.
        """
        for i, path in enumerate(self.dest_dir_files):
            self.dest_dir_files[i] = Path(str(path).replace("_BIS_", ""))
            # path = Path(str(path).replace("_BIS_", ""))

    def get_all_dst_dir_paths(self) -> list:
        """Get all dst dir file paths as a list"""
        files = self.scan_dir(self.dest_dir, True)
        self.dest_dir_files = list(files.keys())

    def get_size(self, path):
        """Get the size of a file in MB."""
        return round(path.stat().st_size / (1024 * 1024), 4)

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
        # print("Target", target)
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        file_dialog.setDirectory(target) # Does not work!!! :(

        # selected_dir = QFileDialog.getExistingDirectory(None, target)

        selected_dir = file_dialog.getExistingDirectory(
            caption="Select a folder"
        )
        target_field.setText(selected_dir)

    def rename_duplicates(self, src_path_dict: dict):
        """Rename file if file with same name exists in the destination dir.

        Creates a new 'final_dest_path' key in the src_path_dict dict that
        holds the final, unique path for this file.

        I am doing it like this, instead of on they fly by listing the dst dir.
        If DRY_RUN is on, files will not be moved to their dst location,
        so each time I list the dst dir to figure out duplicate names I will
        allways get the same list (of the already existing files), thus I will
        never be able to figure out if there are duplicate names.

        The dst_paths list will grow each time we create a new final path.

        src_path_dict (dict): structure:
            {Path(): {"size": float, "temp_dest_path": str}}
        """
        # existing_file_names = copy.copy(self.dest_dir_files) #  I do not want
        #  to copy the list so it grows with the newly created paths.
        src_path_dict["final_dest_path"] = None
        temp_path = src_path_dict["temp_dest_path"]
        root = Path().joinpath(*temp_path.parts[:-1])
        stem = temp_path.stem
        suffix = temp_path.suffix
        # print(temp_path)
        # print(root)

        # print(f"Renaming path {temp_path}")
        """
        Old method: 
          I removed all '_BIS_'s found in all dst paths, 
          then counted the amount of existing equal paths
          then added as many '_BIS_' as the found amount. 
          This is a bit naive as it would easily clash with files that would
          already have '_BIS_' in their name.
          
        count = len([s for s in existing_file_names if s == temp_path])
        stem = stem + ("_BIS_" * count)
        # final_dest_path = self.dest_dir / stem
        final_dest_path = root / stem
        final_dest_path = final_dest_path.with_suffix(suffix)
        src_path_dict["final_dest_path"] = final_dest_path
        """
        """New method:
          I am not removing the '_BIS_' occurrences in the dst paths,
          then in a while loop I am adding '_BIS_' in the new file path until 
          I find a suitable file name.
          In theory this is bulletproof."""
        slot_found = False
        while not slot_found:
            # Build the new path
            final_dest_path = root / stem
            final_dest_path = final_dest_path.with_suffix(suffix)

            # Check if it already exists
            if final_dest_path not in self.dest_dir_files:
                slot_found = True
                src_path_dict["final_dest_path"] = final_dest_path
                self.dest_dir_files.append(final_dest_path)
            stem = stem + "_BIS_"



    def scan_dir(
            self,
            path: Path,
            recursive: bool = True) -> List[Path]:
        """Scans a dir and outputs all documents paths.

        Args:
            path (Path):
            recursive (bool):

        Returns:
            dict : {Path: {"size": int}}
        """
        documents = []

        path_obj = Path(path)

        if recursive:
            # Use rglob for recursive search
            for item in path_obj.rglob("*"):
                if item.is_file():
                    documents.append(item)
        else:
            # Use iterdir for non-recursive search
            for item in path_obj.iterdir():
                if item.is_file():
                    documents.append(item)

        documents = {d: {"size": self.get_size(d)} for d in documents}

        return documents