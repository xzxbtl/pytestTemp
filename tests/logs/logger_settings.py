import copy
import logging
import os
import sys
from colorama import Fore, Style

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
os.makedirs(LOG_DIR, exist_ok=True)


class SafeUnicodeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            if hasattr(stream, 'buffer'):
                stream.buffer.write(msg.encode('utf-8', errors='replace'))
                stream.buffer.write(self.terminator.encode('utf-8'))
            else:
                stream.write(msg)
                stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN + Style.BRIGHT,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        record_copy = copy.copy(record)
        if record_copy.levelno in self.COLORS:
            color = self.COLORS[record_copy.levelno]
            record_copy.levelname = f"{color}{record_copy.levelname}{Style.RESET_ALL}"
            record_copy.msg = f"{color}{record_copy.msg}{Style.RESET_ALL}"
        return super().format(record_copy)


console_handler = SafeUnicodeStreamHandler()
console_handler.setFormatter(ColoredFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
))

file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'app.log'), encoding='utf-8')


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARNING


file_handler.addFilter(InfoFilter())
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d"
))

error_handler = logging.FileHandler(os.path.join(LOG_DIR, 'errors.log'), encoding='utf-8')
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d"
))


class SensitiveFilter(logging.Filter):
    def filter(self, record):
        return not any(word in record.getMessage().lower()
                       for word in ['password', 'token', 'secret'])


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addFilter(SensitiveFilter())
