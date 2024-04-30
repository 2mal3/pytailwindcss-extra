from os import environ
import logging

log = logging.getLogger("pytailwindcss-extra")
log.setLevel(logging.DEBUG)

_formatter = logging.Formatter(
    "[%(asctime)s] [pytailwindcss-extra/%(levelname)s]: %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)

if environ.get("DEBUG"):
    _LEVEL = logging.DEBUG
else:
    _LEVEL = logging.INFO
_console_handler = logging.StreamHandler()
_console_handler.setLevel(_LEVEL)
_console_handler.setFormatter(_formatter)
log.addHandler(_console_handler)
