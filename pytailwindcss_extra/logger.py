import logging

_LEVEL = logging.INFO

log = logging.getLogger("pytailwindcss-extra")
log.setLevel(_LEVEL)

_formatter = logging.Formatter(
    "%(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)

_console_handler = logging.StreamHandler()
_console_handler.setLevel(_LEVEL)
_console_handler.setFormatter(_formatter)
log.addHandler(_console_handler)
