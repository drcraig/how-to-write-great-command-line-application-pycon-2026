import sys
from argparse import ArgumentParser, FileType


def counts(infile):
    line_count = word_count = char_count = 0
    for line in infile:
        line_count += 1
        word_count += len(line.split())
        char_count += len(line)
    return line_count, word_count, char_count


def do(*, infiles, lines, words):
    for infile in infiles:
        line_count, word_count, char_count = counts(infile)

        no_options = not any([lines, words])
        outputs = []
        if no_options or lines:
            outputs.append(line_count)
        if no_options or words:
            outputs.append(word_count)
        if no_options:
            outputs.append(char_count)
        if infile != sys.stdin:
            outputs.append(infile.name)
        yield outputs


def main(raw_args: list[str]) -> int:
    """
    Count newlines, words, and characters
    """
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument("infiles", type=FileType("r"), default=[sys.stdin], nargs="*")
    parser.add_argument(
        "-l", "--lines", action="store_true", help="Print the newline count."
    )
    parser.add_argument(
        "-w", "--words", action="store_true", help="print the word counts"
    )
    args = parser.parse_args(raw_args)

    for output in do(**vars(args)):
        print(f"{' '.join(map(str, output))}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
