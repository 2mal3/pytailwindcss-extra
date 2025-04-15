from sys import exit

from pytailwindcss_extra.main import main
from pytailwindcss_extra.logger import log


if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except Exception as e:
        log.fatal(e)
        exit(1)
