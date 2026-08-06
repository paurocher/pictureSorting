"""Picture Sorting tab."""
from pathlib import Path
from pprint import pprint as pp

from Qt.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ... import globals
from ... import utilities as utils
from .tab import Tab

class Tab01(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.action_name = "Sort Pictures"
        self.about_text = (
            "Sort pictures by date and move them into a year / month / day "
            "folder structure in the selected destination folder."
        )

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()

        self.src_dir_files_pic: dict = {}
        self.src_dir_files_mov: dict = {}

        self.src_field.setText("/home/fuku/Desktop/test")
        self.dst_pic_field.setText("/home/fuku/Desktop/test_pic_trash")
        self.dst_mov_field.setText("/home/fuku/Desktop/test_mov_trash")

    def build_main_ui(self):
        top_ui = QWidget()
        top_layout = QVBoxLayout()
        top_ui.setLayout(top_layout)
        top_ui.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        src_layout = QHBoxLayout()
        top_layout.addLayout(src_layout)
        src_label = QLabel("Source folder: ")
        src_layout.addWidget(src_label)
        self.src_field = QLineEdit()
        src_layout.addWidget(self.src_field)
        browse_src_button = QPushButton("Browse")
        browse_src_button.clicked.connect(lambda: utils.open_file_browser(self.src_field))
        src_layout.addWidget(browse_src_button)

        self.pic_group = QGroupBox("Pictures")
        self.pic_group.setCheckable(True)
        self.pic_group.setChecked(True)
        pic_layout = QGridLayout()
        self.pic_group.setLayout(pic_layout)
        dst_pic_label = QLabel("Destination folder: ")
        pic_layout.addWidget(dst_pic_label, 1, 0)
        self.dst_pic_field = QLineEdit()
        pic_layout.addWidget(self.dst_pic_field, 1, 1)
        browse_dst_pic_button = QPushButton("Browse")
        browse_dst_pic_button.clicked.connect(lambda: utils.open_file_browser(self.dst_pic_field))
        pic_layout.addWidget(browse_dst_pic_button, 1, 2)
        top_layout.addWidget(self.pic_group)

        self.mov_group = QGroupBox("Movies")
        self.mov_group.setCheckable(True)
        self.mov_group.setChecked(False)
        mov_layout = QGridLayout()
        self.mov_group.setLayout(mov_layout)
        dst_mov_label = QLabel("Destination folder: ")
        mov_layout.addWidget(dst_mov_label, 1, 0)
        self.dst_mov_field = QLineEdit()
        mov_layout.addWidget(self.dst_mov_field, 1, 1)
        browse_dst_mov_button = QPushButton("Browse")
        browse_dst_mov_button.clicked.connect(lambda: utils.open_file_browser(self.dst_mov_field))
        mov_layout.addWidget(browse_dst_mov_button, 1, 2)
        top_layout.addWidget(self.mov_group)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        top_layout.addWidget(separator)

        self.top_layout.addWidget(top_ui)

    def run(self):
        """Sort pictures.

        Move image and movie files to appropriate location based on the date.
        Append _BIS_ to duplicate file names to avoid conflicts or overwriting.
        !!DO NOT RUN THIS FROM ALREADY ORGANIZED BY DATE FOLDERS. OTHERWISE, ALL
        FILES WILL HAVE __BIS__ APPENDED TO THEIR NAME!!!"""
        # holds the type of media (pict, mov), its src and dst paths and a
        # custom filter to filter in only the files that adhere to the
        # media type
        media_paths = {
            "picture": {
                "paths": None,
                "filter": utils.is_picture
            },
            "movie": {
                "paths": None,
                "filter": utils.is_movie
            }
        }
        if not self.checks(media_paths):
            self.end()

        for media_type, path_bundle in media_paths.items():
            if not path_bundle["paths"]:
                continue
            src_path = path_bundle["paths"][0]
            dst_path = path_bundle["paths"][1]
            filter = path_bundle["filter"]

            # get paths all from the media src dir
            paths = utils.scan_dir(
                src_path, recursive=self.recursive_checkbox.isChecked()
            )
            # filter the found files with the media filter
            valid_paths = [p for p in paths if filter(p)]
            # print(valid_paths)

            self.terminal.success(
                f"Found {len(valid_paths)} {media_type} items.<br>"
            )

            renamed = []
            not_moved = []
            for i, path in enumerate(valid_paths):
                self.terminal.info(
                    f"\rProcessing item: {i + 1} / {len(valid_paths)}"
                )
                self.terminal.info(str(path))

                dates = utils.get_file_dates(path, media_type)
                # self.terminal.info(str(dates))
                if not dates:
                    self.terminal.error(
                        "No dates. Check file or code because there "
                        "should at least be a date of creation or some "
                        "date!!"
                    )
                    continue
                smallest_date = utils.get_earlier_date(dates)
                # self.terminal.info(f"Smallest date fund: {smallest_date}")

                date_path = utils.build_dates_dst_path(smallest_date)
                new_dst_path = Path(dst_path) / date_path
                file_date_name = smallest_date.strftime("%Y%m%d_%H%M%S")
                full_new_file_path = new_dst_path / file_date_name
                # Figure out duplicate names
                utils.rename_duplicates(full_new_file_path)
                full_new_file_path = full_new_file_path.with_suffix(path.suffix)

                self.terminal.info(f"  new file path: {full_new_file_path}")
        #
        #     if not DRY_RUN:
        #         try:
        #             shutil.move(path, dest_path)
        #         except:
        #             path_parts = os.path.split(path)
        #             path_parts = os.path.splitext(path_parts[-1])
        #             new_file_name = "".join([path_parts[0], "__BIS__", path_parts[1]])
        #             new_file_dest_path = os.path.join(dest_path, new_file_name)
        #             try:
        #                 shutil.move(path, new_file_dest_path)
        #                 renamed.append([path, new_file_dest_path])
        #             except:
        #                 not_moved.append(path)
        #                 continue
        #             # print()
        # if renamed:
        #     pp(renamed)
            if len(media_paths) > 1:
                self.terminal.info("\n-- -- --\n")

        self.end()


    def checks(self, media_paths) -> bool:
        """Run all tests on the paths. Populate / modify media_paths.

        Returns:
            bool
        """
        if not self.pic_group.isChecked() and not self.mov_group.isChecked():
            self.terminal.warning(
                "Please select at least one type of media to process."
            )
            return False

        dst_pick_check, dst_mov_check = True, True
        check_messages = []
        # path field is not empty, path exists, path is dir
        src_check, messages, src_path = utils.check_paths(
            self.src_field, "Source Field"
        )
        check_messages.append(messages)

        if self.pic_group.isChecked():
            # check path field
            dst_pic_check, messages, dst_pic_path = utils.check_paths(
                self.dst_pic_field, "Pictures Destination Field"
            )
            check_messages.append(messages)
            if all([src_check, dst_pick_check]):
                media_paths["picture"]["paths"] = (src_path, dst_pic_path)
        else:
            media_paths.pop("picture")

        if self.mov_group.isChecked():
            # check path field
            dst_mov_check, messages, dst_mov_path = utils.check_paths(
                self.dst_mov_field, "Movies Destination Field"
            )
            check_messages.append(messages)
            if all([src_check, dst_mov_check]):
                media_paths["movie"]["paths"] = (src_path, dst_mov_path)
        else:
            media_paths.pop("movie")

        # assert that all tests passed
        if not all([src_check, dst_pic_check, dst_mov_check]):
            check_messages = [m for m in check_messages if m]
            self.terminal.warning("<br>".join(check_messages))
            return False

        return True

    def end(self):
        """This is the end, my only fiend, the end."""
        self.terminal.info(f"\n{'- ' * 40}\n")

