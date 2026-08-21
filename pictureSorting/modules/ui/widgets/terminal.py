"""Terminal output."""
from pathlib import Path

from Qt.QtWidgets import QTextEdit


class Terminal(QTextEdit):
    log_file_path = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setReadOnly(True)

    def error(self, text: str) -> None:
        prefix = "<span style='color: #333333; background-color: #DB0B0B;'><b>"
        self.append(f"{prefix}{text}")
        self.write_to_log(f"error: {text}")

    def info(self, text: str) -> None:
        prefix = ""
        self.append(f"{prefix}{text}")
        self.write_to_log(f"info: {text}")

    def success(self, text: str) -> None:
        prefix = "<span style='color: #AAAAAA; background-color: #099400;'><b>"
        self.append(f"{prefix}{text}")
        self.write_to_log(f"success: {text}")

    def warning(self, text: str) -> None:
        prefix = "<span style='color: #555555; background-color: #FCC500;'><b>"
        self.append(f"{prefix}{text}")
        self.write_to_log(f"warning: {text}")

    def write_to_log(self, message: str) -> None:
        """Append message to log file.

        Args:
            message(str): message to append
        """
        with Terminal.log_file_path.open("a") as f:
            f.write(f"\n{self.parent.action_name} :: {message}")

    def create_log_file(self):
        """Create the log file.

        Each time the application is launched a log file will be created in:
        /home/[username]/.pictureSorter/YYYYDDMMHHMMSS.log


        Args:
            log_file_path(str): path to log file
        """
        datetime = self.parent.parent.datetime

        log_dir_path = Path().home() / ".pictureSorter"
        if not log_dir_path.exists():
            log_dir_path.mkdir()

        log_file_name = datetime.strftime("%Y%m%d_%H%M%S")
        log_file_path = log_dir_path / log_file_name
        Terminal.log_file_path = log_file_path.with_suffix(".log")

        if Terminal.log_file_path.exists():
            return False

        Terminal.log_file_path.write_text(f"Log file created on {datetime}")

        self.info(f"Created log file: {datetime}")
