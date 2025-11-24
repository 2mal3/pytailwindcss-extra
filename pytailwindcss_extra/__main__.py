from sys import exit as sys_exit

from pytailwindcss_extra.main import main
from pytailwindcss_extra.logger import log


if __name__ == "__main__":
    try:
        exit_code = main()
        sys_exit(exit_code)
    except KeyboardInterrupt:
        log.info("Exiting...")
        sys_exit(0)
    except Exception as e:
        log.fatal(e)
        sys_exit(1)
