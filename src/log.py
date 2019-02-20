"""Helper methods to configure the system logger."""
import logging
import warnings

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLOURS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColourFormatter(logging.Formatter):
    """Formats log messages using ANSI escape codes."""
    def __init__(self, *args, **kwargs): # type: ignore
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if record.levelname in COLOURS:
            msg = "\033[1;3%dm%s\033[0m" % (COLOURS[record.levelname], msg)
        return msg


def configure() -> None:
    """Configure the root logger. This should be called once when the program is
       initialised.

    """
    # Be more aggressive in capturing warnings
    logging.captureWarnings(True)
    warnings.simplefilter('default')

    logger = logging.getLogger()

    # Register a custom formatter, which prints things coloured with the time, level and coponent name.
    formatter = ColourFormatter("[%(asctime)s] [%(levelname)s/%(name)s] %(message)s", None, '%')
    formatter.default_msec_format = "%s.%03d"

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
