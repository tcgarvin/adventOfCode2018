from argparse import ArgumentParser
import fileinput

def parse_line(line):
    return line

def parse_input(lines):
    return map(parse_line, lines)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()

    parsed = parse_input(fileinput.input(args.file))

    print(list(parsed))