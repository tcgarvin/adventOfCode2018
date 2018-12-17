from argparse import ArgumentParser
import fileinput

def parse_line(line):
    return line

def parse_input(lines):
    return list(map(parse_line, lines))


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    puzzle_input = parse_input(fileinput.input(args.file))

    # Part 1
    part1 = "Unknown"

    print("Part 1:", part1)


    # Part 2
    part2 = "Unknown"

    print("Part 2:", part2)