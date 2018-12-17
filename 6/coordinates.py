from argparse import ArgumentParser
from collections import defaultdict
import fileinput

def parse_line(line):
    l = line.split(",")
    return (int(l[0]), int(l[1]))

def parse_input(lines):
    return list(map(parse_line, lines))

def evaluate_position(y,x,coordinate_pairs, world):
    if world[y][x] is not None:
        return

    max_y = len(world)
    max_x = len(world[0])
    closest_coordinate = None
    min_distance = max_y + max_x
    second_min_distance = min_distance
    for pair in coordinate_pairs:
        distance = abs(y - pair[1]) + abs(x - pair[0])
        if distance < min_distance:
            second_min_distance = min_distance
            min_distance = distance
            closest_coordinate = pair
        elif distance == min_distance:
            closest_coordinate = "TIE"
        elif distance < second_min_distance:
            second_min_distance = distance

    world[y][x] = closest_coordinate

    #if closest_coordinate != "TIE":
    #    leeway = (second_min_distance - min_distance - 2) // 2  # Thinking about Aa.bB

    #    # Mark everything in the following pattern:
    #    # Given leeway of 3:
    #    #
    #    # aaaaaabbbbb
    #    # aAx.......B
    #    # ...........
    #    # ...........
    #    # ...........
    #    # becomes:
    #    #
    #    # aaaaaabbbbb
    #    # aAxaaa....B
    #    # aaaaa......
    #    # .aaa.......
    #    # ..a........

    #    for dy in range(leeway + 1):
    #        ty = y + dy
    #        if ty >= max_y:
    #            continue
    #        
    #        plusminus = leeway - dy
    #        for dx in range(-plusminus, plusminus + 1):
    #            tx = x + dx
    #            if tx < 0 or tx >= max_x:
    #                continue
    #            
    #            assert world[ty][tx] in (None, closest_coordinate)
    #            world[ty][tx] = closest_coordinate


def generate_closest(coordinate_pairs):
    # Part 1
    xs, ys = zip(*coordinate_pairs)
    max_x = max(xs) + 1
    max_y = max(ys) + 1

    world = [[None for x in range(max_x)] for y in range(max_y)]

    for y in range(max_y):
        for x in range(max_x):
            evaluate_position(y, x, coordinate_pairs, world)

    return world

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    coordinate_pairs = parse_input(fileinput.input(args.file))

    # Part 1
    world = generate_closest(coordinate_pairs)
    for row in world:
        print(row)

    infinite_ranges = set()
    range_sizes = defaultdict(int)
    y_size = len(world)
    x_size = len(world[0])
    for y in range(y_size):
        for x in range(x_size):
            nearest = world[y][x]
            if nearest == "TIE":
                continue

            range_sizes[nearest] += 1
            
            if y == 0 or y + 1 == y_size or x == 0 or x + 1 == x_size:
                infinite_ranges.add(nearest)

    max_size = 0
    for pair, size in range_sizes.items():
        if size > max_size and pair not in infinite_ranges:
            max_size = size
    print("Part 1:", max_size)


    # Part 2
    safe_spaces = 0
    for x in range(x_size):
        for y in range(y_size):
            distance_sum = 0
            for pair in coordinate_pairs:
                distance_sum += abs(x-pair[0]) + abs(y-pair[1])
            if distance_sum < 10000:
                safe_spaces += 1

    print("Part 2:", safe_spaces)