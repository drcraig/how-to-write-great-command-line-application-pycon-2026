import logging
import os
import sys
from argparse import ArgumentParser
from time import sleep

logger = logging.getLogger(__name__)


def fibonnaci():
    a, b = 0, 1
    while True:
        yield a
        logger.info("Calculating next value after %s", a)
        a, b = b, a + b
        logger.warning("Next one will be big")


def main(raw_args: list[str]) -> int:
    """Prints the fibonnaci sequence"""
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    args = parser.parse_args(raw_args)

    level = max(logging.ERROR - args.verbosity * 10, logging.NOTSET)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")

    for value in fibonnaci():
        print(value, flush=True)
        sleep(0.2)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)
