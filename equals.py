import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="Compare two values")
parser.add_argument("first")
parser.add_argument("second")
args = parser.parse_args()

if args.first == args.second:
    sys.exit(0)
sys.exit(1)
