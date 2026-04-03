import logging
import os
import sys
import shutil
from typing import Optional
from colorama import Fore, Style, init

# Initialisiert Colorama für die farbige Terminal-Ausgabe
init(autoreset=True)

# Globale Variable für den Standard-Speicherort
_DEFAULT_LOG_DIR = "logs"


class ColorFormatter(logging.Formatter):
    """
    Block-Formatter mit Datum: [YYYY-MM-DD HH:MM:SS] | LEVEL | (Context) location - Message
    Ganze Zeile farbig, INFO = Blau, DEBUG = Cyan.
    """

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        level_color = self.COLORS.get(record.levelno, "")
        asctime = self.formatTime(record, datefmt='%Y-%m-%d %H:%M:%S')

        # Anpassung: Padding entfernt bzw. auf ein Minimum reduziert (Level 5 Zeichen)
        level_name = f"{record.levelname:5}"
        context = f"({record.name})"
        location = f"{record.filename}:{record.lineno}"

        log_fmt = (
            f"{Style.DIM}[{asctime}]{Style.RESET_ALL} |"
            f"{level_color}{level_name}{Style.RESET_ALL}| "
            f"{context} "
            f"{Style.DIM}{location}{Style.RESET_ALL} - "
            f"{level_color}%(message)s{Style.RESET_ALL}"
        )

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_logging(log_dir: str, clear_old_logs: bool = False) -> None:
    """
    Setzt den globalen Standard-Speicherort fest.
    :param log_dir: Pfad zum Log-Ordner.
    :param clear_old_logs: Wenn True, wird der Ordner beim Start komplett geleert.
    """
    global _DEFAULT_LOG_DIR
    _DEFAULT_LOG_DIR = log_dir

    if clear_old_logs and os.path.exists(log_dir):
        # Löscht alle Dateien im Log-Ordner
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Fehler beim Löschen von {file_path}: {e}")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def get_logger(
        name: str,
        filename: Optional[str] = None,
        log_dir: Optional[str] = None,
        level: int = logging.INFO,
        clear: bool = True  # Standardmäßig Datei beim Start leeren
) -> logging.Logger:
    """
    Erstellt oder holt einen konfigurierten Logger.
    :param clear: Wenn True (default), wird die Datei überschrieben statt angehängt.
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # 1. HANDLER: KONSOLE
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    # 2. HANDLER: DATEI
    if filename:
        target_dir = log_dir if log_dir is not None else _DEFAULT_LOG_DIR
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        full_path = os.path.join(target_dir, filename)

        # mode='w' überschreibt die Datei (Clear beim Start)
        # mode='a' würde neue Logs unten anfügen
        file_mode = 'w' if clear else 'a'

        # Auch hier das Padding für die Datei entfernt
        file_format = logging.Formatter(
            '[%(asctime)s] |%(levelname)5s| (%(name)s) %(filename)s:%(lineno)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = logging.FileHandler(full_path, encoding='utf-8', mode=file_mode)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


# --- EXAMPLE USAGE (Uncomment to test) ---
"""
if __name__ == "__main__":
     # 1. Setup: Define where to save logs and if old ones should be deleted
     configure_logging(log_dir="test_logs", clear_old_logs=True)

     # 2. Create Loggers for different parts of your app
     log_srv = get_logger("Server", filename="system.log", level=logging.DEBUG)
     log_db  = get_logger("Database") # Default level is INFO

     # 3. Start logging
     log_srv.debug("This is a debug message (Cyan)")
     log_srv.info("This is an info message (Blue)")
     log_srv.warning("This is a warning (Yellow)")
     log_srv.error("This is an error (Red)")
     log_srv.critical("This is critical (Bold Red)")
"""