from itertools import cycle
from math import lcm

from myiters import ChainIterable


directions = {
    "L": 0,
    "R": 1,
}


def get_way(way_line):
    return map(directions.__getitem__, way_line.strip())


def get_nodes(lines):
    return (
        ChainIterable(lines)
            .map(str.strip)
            .filter(bool)
            .map(lambda line: line.split(" = "))
            .tuple_map(lambda name, pair: (name, pair.strip("()").split(", ")))
            .to_dict()
    )


def task1(filename):
    with open(filename) as file:
        way = get_way(next(file))
        nodes = get_nodes(file)

    point = "AAA"
    end = "ZZZ"
    for step, direction in enumerate(cycle(way)):
        if point == end:
            return step
        point = nodes[point][direction]


def task2(filename):
    with open(filename) as file:
        way = get_way(next(file))
        nodes = get_nodes(file)

    points = [node for node in nodes if node.endswith("A")]
    steps = []
    for step, direction in enumerate(cycle(way)):
        if any(point.endswith("Z") for point in points):
            steps.append(step)
        points = [nodes[point][direction] for point in points if not point.endswith("Z")]
        if not points:
            break

    return lcm(*steps)


if __name__ == "__main__":
    filename = "inputs/day8.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
