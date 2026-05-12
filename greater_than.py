import sys
from argparse import ArgumentParser


def main(raw_args: list[str]) -> int:
    parser = ArgumentParser()
    parser.add_argument("first")
    parser.add_argument("second")
    args = parser.parse_args(raw_args)

    if args.first > args.second:
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

