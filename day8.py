from itertools import cycle
from math import lcm


directions = {
    "L": 0,
    "R": 1,
}


def task1(filename):
    start = "AAA"
    end = "ZZZ"
    nodes = {}
    with open(filename) as file:
        way = next(file).strip()
        for line in file:
            line = line.strip()
            if not line:
                continue
            name, pair = line.split(" = ")
            left, right = pair.strip("()").split(", ")
            nodes[name] = (left, right)

    for step, direction in enumerate(cycle(way), start=1):
        start = nodes[start][directions[direction]]
        if start == end:
            return step


def task2(filename):
    points = []
    nodes = {}
    with open(filename) as file:
        way = next(file).strip()
        for line in file:
            line = line.strip()
            if not line:
                continue
            name, pair = line.split(" = ")
            left, right = pair.strip("()").split(", ")
            nodes[name] = (left, right)
            if name.endswith("A"):
                points.append(name)

    steps = []
    for step, direction in enumerate(cycle(way)):
        if any(point.endswith("Z") for point in points):
            steps.append(step)
        points = [nodes[point][directions[direction]] for point in points if not point.endswith("Z")]
        if not points:
            break

    return lcm(*steps)


if __name__ == "__main__":
    filename = "inputs/day8.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
