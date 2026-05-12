import sys
from argparse import ArgumentParser
from contextlib import nullcontext
from io import IOBase
from pathlib import Path


def open_file_or_io(file_path_or_io, *args, **kwargs):
    """Return the open() context manager for a file,
    or a null context manager an existing file object."""
    if isinstance(file_path_or_io, IOBase):
        return nullcontext(file_path_or_io)
    return open(file_path_or_io, *args, **kwargs)


def PathOrStreamType(stream):
    """Factory function to create a type that will
    use a stream if the argument is "-", otherwise
    cast the argument into a Path."""

    def _path_or_stream(arg):
        if arg == "-":
            return stream
        return Path(arg)

    return _path_or_stream


"""
parser = ArgumentParser()
parser.add_argument(
    "outfile",
    type=PathOrStreamType(sys.stdout),
    default=sys.stdout,
    nargs="?"
)

args = parser.parse_args([])
args = parser.parse_args(["-"])
args = parser.parse_args(["foo.txt"])

with open_file_or_io(args.outfile, 'w') as fobj:
    fobj.write("foo")
"""
