from argparse import ArgumentParser
import fileinput

from itertools import cycle

def parse_line(line):
    return int(line)

def parse_input(lines):
    return list(map(parse_line, lines))


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()

    parsed = parse_input(fileinput.input(args.file))

    total = 0
    for num in parsed:
        total += num

    print("Part 1: " + str(total))

    current_frequency = 0
    frequencies = set()
    for frequency_change in cycle(parsed):
        current_frequency += frequency_change
        if current_frequency in frequencies:
            break
        frequencies.add(current_frequency)

    print("Part 2: " + str(current_frequency))
