from argparse import ArgumentParser
from collections import defaultdict
import fileinput
from functools import reduce

class Shift(object):

    def __init__(self):
        self.edges = []
        self.awake_index = None
        self.state = None

    def start(self, day, guard):
        assert self.state is None
        self.guard = guard
        self.day = day
        self.state = "awake"

    def sleep(self, day, minute):
        assert self.state is "awake"
        self.day = day
        self.edges.append(minute)
        self.state = "asleep"

    def awake(self, day, minute):
        assert self.state is "asleep"
        self.day = day
        self.edges.append(minute)
        self.state = "awake"

    def isAwake(minute):
        awake = True
        for edge in self.edges:
            if minute < edge:
                return awake
            awake = not awake
        return awake

    def ensureAwakeIndex(self):
        if self.awake_index is not None:
            return

        self.awake_index = []
        cursor = 0
        awake = True
        for edge in (self.edges + [60]):
            for minute in range(cursor, edge):
                self.awake_index.append(awake)
            awake = not awake
            cursor = edge

    def __str__(self):
        self.ensureAwakeIndex()
        return "{0} {1:>5}: {2}".format(
            self.day, 
            self.guard, 
            "".join((("." if awake else "#") for awake in self.awake_index)))

def print_shifts(shifts):
    print(" " * 18 + "".join((n * 10) for n in "012345"))
    print(" " * 18 + "0123456789" * 6)
    for shift in shifts:
        print(shift)
    
def get_day(line):
    return line.split()[0][1:]

def get_minute(line):
    return int(line.split()[1][3:5])
        
def parse_input(lines):
    shift = None
    shifts = []
    for line in sorted(lines):
        #print(line)
        if "begins" in line:
            shift = Shift()
            shift.start(get_day(line), line.split()[3])
            shifts.append(shift)

        elif "asleep" in line:
            shift.sleep(get_day(line), get_minute(line))
        
        elif "wakes" in line:
            shift.awake(get_day(line), get_minute(line))

        else:
            print("(No-op)")

    return shifts

def total_nights_sleep(shift):
    return reduce(lambda total, a: total + (0 if a else 1), shift.awake_index, 0)

def calculate_sleepiest_minute(shifts):
    totals = [0] * 60
    for shift in shifts:
        for minute in range(60):
            totals[minute] += (0 if shift.awake_index[minute] else 1)

    #print(totals)

    result = None
    most_instances = 0
    for minute, instances in enumerate(totals):
        if instances > most_instances:
            #print(minute, instances)
            most_instances = instances
            result = minute

    return result, most_instances


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    shifts = parse_input(fileinput.input(args.file))

    print_shifts(shifts)
    print()

    # Part 1
    part1 = "Unknown"

    guard_sleep_totals = defaultdict(int)
    for shift in shifts:
        guard_sleep_totals[shift.guard] += total_nights_sleep(shift)

    #print(guard_sleep_totals)

    sleepiest_guard = None
    most_sleep = 0
    for guard, sleep in guard_sleep_totals.items():
        if sleep > most_sleep:
            most_sleep = sleep
            sleepiest_guard = guard

    #print(sleepiest_guard, most_sleep)

    sleepiest_minute, instances = calculate_sleepiest_minute(filter(lambda s: s.guard == sleepiest_guard, shifts))

    print("Part 1: " + str(int(sleepiest_guard[1:]) * sleepiest_minute))


    # Part 2
    guards = set()
    for shift in shifts:
        guards.add(shift.guard)

    result_guard = None
    result_minute = None
    most_instances = 0
    for guard in guards:
        sleepiest_minute, instances = calculate_sleepiest_minute(filter(lambda s: s.guard == guard, shifts))
        if instances > most_instances:
            result_guard = guard
            result_minute = sleepiest_minute
            most_instances = instances

    print("Part 2: " + str(int(result_guard[1:]) * result_minute))