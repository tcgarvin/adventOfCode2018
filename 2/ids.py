from argparse import ArgumentParser
from collections import defaultdict
from itertools import combinations
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
    twos = 0
    threes = 0
    for line in puzzle_input:
        letter_count = defaultdict(int)

        for letter in line:
            letter_count[letter] += 1

        found_twos = False
        found_threes = False
        for letter, count in letter_count.items():
            if count == 2:
                found_twos = True

            if count == 3:
                found_threes = True

        if found_twos:
            twos += 1

        if found_threes:
            threes += 1

    print("Part 1: " + str(twos * threes))


    # Part 2
    candidates = []
    for id1, id2 in combinations(puzzle_input, 2):
        differences = 0
        for a, b in zip(id1, id2):
            if a != b:
                differences += 1

            if differences > 1:
                break

        if differences == 1:
            candidates = [id1, id2]
            break

    part2 = ""
    for a,b in zip(candidates[0], candidates[1]):
        if a == b:
            part2 = part2 + a

    print("Part 2: " + str(part2))