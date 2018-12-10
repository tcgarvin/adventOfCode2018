from argparse import ArgumentParser
from collections import defaultdict
import fileinput
import re

CLAIM_RE = re.compile("""
  [#](?P<id>[0-9]+)
  [ ][@][ ]
  (?P<x>[0-9]+),(?P<y>[0-9]+)
  :[ ]
  (?P<w>[0-9]+)x(?P<h>[0-9]+) 
""", re.X)

def parse_line(line):
    result = CLAIM_RE.match(line).groupdict()
    result["x"] = int(result["x"])
    result["y"] = int(result["y"])
    result["w"] = int(result["w"])
    result["h"] = int(result["h"])
    return result

def parse_input(lines):
    return list(map(parse_line, lines))


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    puzzle_input = parse_input(fileinput.input(args.file))

    # Part 1
    fabric = defaultdict(lambda: defaultdict(set))
    for claim in puzzle_input:
        cid = claim["id"]
        x_orig = claim["x"]
        y_orig = claim["y"]
        w = claim["w"]
        h = claim["h"]
        for y in range(y_orig, y_orig + h):
            for x in range(x_orig, x_orig + w):
                fabric[x][y].add(cid)

    overlaps = 0
    for row in fabric.values():
        for cell in row.values():
            if len(cell) > 1:
                overlaps += 1

    print("Part 1: " + str(overlaps))


    # Part 2

    valid_claims = set((claim["id"] for claim in puzzle_input))
    overlaps = 0
    for row in fabric.values():
        for cell in row.values():
            if len(cell) > 1:
                valid_claims -= cell

    print("Part 2: " + str(valid_claims))