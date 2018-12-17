from argparse import ArgumentParser
import fileinput

class Node(object):
    def __init__(self):
        self.subnodes = []
        self.metadata = []

    def set_metadata(self, metadata):
        self.metadata = metadata

    def add_subnode(self, subnode):
        self.subnodes.append(subnode)

def parse_input(lines):
    for line in lines:
        return list(map(int, line.split()))

def parse_node(integers):
    num_subnodes = integers[0]
    num_metadata = integers[1]

    node = Node()

    remainder = integers[2:]
    for i in range(num_subnodes):
        subnode, remainder = parse_node(remainder)
        node.add_subnode(subnode)

    node.set_metadata(remainder[:num_metadata])
    return node, remainder[num_metadata:]

def sum_metadata(tree):
    return sum(tree.metadata) + sum((sum_metadata(subnode) for subnode in tree.subnodes))

def print_tree(node, depth=0):
    print(" " * depth, " ".join(map(str, node.metadata)))
    for subnode in node.subnodes:
        print_tree(subnode, depth + 2)

def extract_value(node):
    if len(node.subnodes) == 0:
        return sum(node.metadata)

    total = 0
    for metadatum in node.metadata:
        if metadatum == 0 or metadatum > len(node.subnodes):
            continue
        
        total += extract_value(node.subnodes[metadatum - 1])

    return total


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    integers = parse_input(fileinput.input(args.file))

    # Part 1
    tree, leftovers = parse_node(integers)
    #print_tree(tree)
    assert len(leftovers) == 0
    print("Part 1:", sum_metadata(tree))


    # Part 2
    root_value = extract_value(tree)
    print("Part 2:", root_value)