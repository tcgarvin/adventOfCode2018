from argparse import ArgumentParser
import fileinput

def parse_line(line):
    split = line.split()
    return (split[1], split[7])

def parse_input(lines):
    return list(map(parse_line, lines))

class Step(object):
    @staticmethod
    def generate_from_edges(edges):
        nodes = {}
        for edge in edges:
            node_a = nodes.setdefault(edge[0], Step(edge[0]))
            node_b = nodes.setdefault(edge[1], Step(edge[1]))
            node_b.add_dependency(node_a)

        return list(nodes.values())

    def __init__(self, name):
        self.name = name
        self._complete = False
        self.dependencies = set()
        self.dependents = set()

    def add_dependency(self, step):
        self.dependencies.add(step)
        step.dependents.add(self)

    def is_available(self):
        for dependency in self.dependencies:
            if not dependency.is_complete():
                return False

        return True

    def is_complete(self):
        return self._complete

    def complete(self):
        if not self.is_available():
            raise Exception("Can't complete this step, other steps pending")
        self._complete = True

    def run_time(self):
        return ord(self.name) - ord("A") + 1

class Worker(object):
    def __init__(self, id):
        self.id = id
        self.step = None
        self.finish_at = float("inf")

    def step_string(self):
        return "." if self.step is None else self.step.name


def find_execution_order(nodes):
    execution_order = []
    available = []
    for node in nodes:
        if node.is_available():
            available.append(node)


    while len(available) > 0:
        available = sorted(available, key=lambda n: n.name, reverse=True)
        #print("  Available:", node_list_string(available))
        first_available = available.pop()
        first_available.complete()
        execution_order.append(first_available)

        #print("Executed:", node_list_string(execution_order))

        added = []
        for dependent in first_available.dependents:
            if dependent.is_available():
                assert dependent not in available
                available.append(dependent)
                added.append(dependent)

        #print("  Newly available:", node_list_string(added))

    return execution_order

def node_list_string(nodes):   
    return "".join(map(lambda n: n.name, nodes))

def execute_in_parallel(nodes, num_workers=1, base_duration=0):
    workers = [Worker(i) for i in range(num_workers)]

    format_string = "{:>8} " + "{:^5}" * num_workers + "{:^" + str(len(nodes) + 2) + "}{:^10}"
    print(format_string.format("Second", *["W"+str(i) for i in range(num_workers)], "Done", "Available"))

    available = []
    running = []
    done = []
    for node in nodes:
        if node.is_available():
            available.append(node)

    second = 0
    while len(available) > 0 or len(running) > 0:
        for worker in workers:
            if worker.finish_at == second:
                worker.step.complete()
                done.append(worker.step)
                for dependent in worker.step.dependents:
                    if dependent.is_available():
                        assert dependent not in available
                        available.append(dependent)

                worker.step = None
                worker.finish_at = float("inf")

        unassigned_workers = filter(lambda w: w.step is None, workers)
        available = sorted(available, key=lambda n: n.name, reverse=True)

        new_assignments = list(zip(unassigned_workers, available))
        for worker, step in new_assignments:
            available.remove(step)
            worker.step = step
            worker.finish_at = second + step.run_time() + base_duration

        running = list(map(lambda w: w.step, filter(lambda w: w.step is not None, workers)))

        print(format_string.format(second, *[w.step_string() for w in workers], node_list_string(done), node_list_string(available)))

        second += 1

    return second - 1


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file', metavar='FILE', nargs="?", default="-")
    args = arg_parser.parse_args()
    edges = parse_input(fileinput.input(args.file))

    # Part 1
    nodes = Step.generate_from_edges(edges)
    execution_order = find_execution_order(nodes)

    print("Part 1:", "".join(map(lambda n: n.name, execution_order)))


    # Part 2
    nodes = Step.generate_from_edges(edges)
    time = execute_in_parallel(nodes, num_workers=5, base_duration=60)

    print("Part 2:", time)