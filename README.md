# how-to-write-great-command-line-application-pycon-2026

Code samples from my PyCon US 2026 talk "How To Write a Great Command Line Application" ([Slides](<How To Write a Great Command Line Application.pdf>))

1. [print_args.py](print_args.py)
2. [equals.py](equals.py)
3. [greater_than.py](greater_than.py)
4. [wc.py](wc.py)
5. [file_type_replacements.py](file_type_replacements.py)
6. [fibonacci.py](fibonacci.py)

Good patterns to follow with argparse:
* Use a shebang with uv to specify your third party dependencies.
* Use a `main()` function that takes a list of raw arguments and returns the exit code.
* Use `main.__doc__` to deduplicate your docstrings and your help text.
* Call your main function under dunder main and pass its return value to `sys.exit()`.
* Catch and handle `KeyboardInterrupt` and `BrokenPipeErrors` to make your program play nicely with others.
* Use a `do()` function that takes all of your argparse arguments using keyword-only arguments with `**vars()`, and yield each line or chunk of output.
* Use logging for verbose debugging output.

Demonstrating all the patterns
```python
#! /usr/bin/env -S uv run --script
#
# /// script
# requires-python = "==3.13"
# dependencies = ["requests"]
# ///
import logging
import os
import sys
from argparse import ArgumentParser, FileType

logger = logging.getLogger(__name__)


def do(*, infiles, upper: bool):
    for infile in infiles:
        for line in infile:
            if upper:
                yield line.upper()
            else:
                yield line


def main(raw_args: list[str]) -> int:
    """Repeats a line"""
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument("infiles", type=FileType("r"), default=[sys.stdin], nargs="*")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-u", "--upper", action="store_true")
    args = vars(parser.parse_args(raw_args))

    verbosity = args.pop("verbosity")
    level = max(logging.ERROR - verbosity * 10, logging.NOTSET)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")

    for output in do(**args):
        print(output, end="", flush=True)

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
```

Alternatives to FileType?
```python
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
```
```python
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
```
