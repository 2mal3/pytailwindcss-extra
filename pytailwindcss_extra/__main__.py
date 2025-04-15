from sys import exit

from pytailwindcss_extra.main import main
from pytailwindcss_extra.logger import log


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.fatal(e)
        exit(1)
