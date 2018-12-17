from argparse import ArgumentParser
import fileinput

CAP_DISTANCE = ord("a") - ord("A")

class PolymerSegment(object):
    @staticmethod
    def from_string(polymer_string):
        first_segment = None
        prev_segment = None
        for char in (" " + polymer_string + " "):
            segment = PolymerSegment(char)
            if first_segment is None:
                first_segment = segment

            if prev_segment is not None:
                segment.prev = prev_segment
                segment.prev.next = segment

            prev_segment = segment

        return first_segment

    def __init__(self, char):
        self.char = char
        self.next = None
        self.prev = None

    def compatible(self, other):
        if other is None:
            return False
        return abs(ord(self.char) - ord(other.char)) == CAP_DISTANCE

    def react(self):
        current = self
        iteration = 0
        while current is not None:
            #visual = ""
            #cursor = 0
            #if iteration % 10000 == 0:
            #    visual, cursor = current.generate_string_with_cursor()
            #    if len(visual) < 80:
            #        print()
            #        print(cursor)
            #        print(visual)

            #    print("{:.2f}%".format(len(cursor) / len(visual) * 100))

            next_up = current.next

            if current.compatible(current.prev):
                #if iteration % 10000 == 0:
                #    print("Remove", current.char, current.prev.char)
                current.prev.prev.next = current.next
                current.next.prev = current.prev.prev
            
            elif current.compatible(current.next):
                #if iteration % 10000 == 0:
                #    print("Remove", current.char, current.next.char)
                next_up = current.next.next
                current.prev.next = current.next.next
                current.next.next.prev = current.prev

            current = next_up
            iteration += 1


    def generate_string_with_cursor(self):
        out = []
        segment = self
        spaces = 0

        while segment.prev is not None:
            segment = segment.prev
            spaces += 1

        while segment is not None:
            out.append(segment.char)
            segment = segment.next
        return ("".join(out)), (" " * spaces + "*")

    def __str__(self):
        visual, cursor = self.generate_string_with_cursor()
        return visual

def parse_input(lines):
    for line in lines:
        return line.strip()

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    initial_polymer_string = parse_input(fileinput.input(args.file))
    initial_polymer = PolymerSegment.from_string(initial_polymer_string)

    # Part 1
    initial_polymer.react()
    print("'" + str(initial_polymer) + "'")
    print("Part 1:", len(str(initial_polymer)) - 2)


    # Part 2
    best_candidate = None
    shortest_length = len(initial_polymer_string)
    for candidate in "abcdefghijklmnopqrstuvwxyz":
        candidate_poly_string = initial_polymer_string.replace(candidate, "").replace(candidate.upper(), "")
        candidate_polymer = PolymerSegment.from_string(candidate_poly_string)
        candidate_polymer.react()
        if len(str(candidate_polymer)) < shortest_length:
            best_candidate = candidate_polymer
            shortest_length = len(str(candidate_polymer))

    print("Part 2:", shortest_length - 2)