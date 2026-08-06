"""Convert HEIF to JPG."""
from .tab import Tab

class Tab02(Tab):
    def __init__(self, parent):
        super().__init__(parent)

        self.action_name = "Convert HEIF to JPG NOT IMPLEMENTED YET"
        self.about_text = "Convert HEIF to JPG"

        self.build_title_ui()
        self.build_main_ui()
        self.build_execute_ui()
        self.build_terminal_ui()

    def run(self):
        """Convert HEIF to JPG."""

        self.terminal.info("NOT IMPLEMENTED YET")

        # source_folder = "/home/fuku/Desktop/100CANON"
        #
        # all_files = utilities.scan_dir(source_folder)
        # heif_files = [file for file in all_files if
        #     os.path.splitext(file)[1].lower() in [".heic", ".heif"]]
        #
        # for i, file in enumerate(heif_files):
        #     heif_file = read_heif(file)
        #
        #     new_file_name = os.path.split(file)
        #     new_file_name_ext = os.path.splitext(new_file_name[-1])
        #     new_file_name = "{}_fromHEIF.jpg".format(new_file_name_ext[0])
        #     dest_path = os.path.join(os.path.split(file)[0], new_file_name)
        #     print("{}/{}  {} --> {}".format(
        #         i,
        #         len(heif_files),
        #         file,
        #         dest_path)
        #     )
        #     heif_to_jpg(heif_file, dest_path)