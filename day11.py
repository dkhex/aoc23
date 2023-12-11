from itertools import combinations

from myiters import ChainIterable


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def offset_x(self, offset_x):
        self.x += offset_x
    
    def offset_y(self, offset_y):
        self.y += offset_y


def task1(filename):
    with open(filename) as file:
        lines = file.readlines()

    height = len(lines)
    width = len(lines[0])

    galaxies = (
        ChainIterable(lines)
            .enumerate()
            .tuple_map(lambda row, string:
                ChainIterable(string)
                    .enumerate()
                    .filter(lambda tup: tup[1] == "#")
                    .tuple_map(lambda col, sym: Coords(col, row))
                    .collect()
            )
            .flat()
            .collect()
    )

    expandable_rows = sorted( set(range(height + 1)) - set(map(Coords.get_y, galaxies)) )
    expandable_cols = sorted( set(range(width + 1)) - set(map(Coords.get_x, galaxies)) )

    inc = 0
    for galaxy in galaxies:
        while galaxy.y > expandable_rows[inc]:
            inc += 1
        galaxy.offset_y(inc)

    galaxies = sorted(galaxies, key=Coords.get_x)

    inc = 0
    for galaxy in galaxies:
        while galaxy.x > expandable_cols[inc]:
            inc += 1
        galaxy.offset_x(inc)

    dist = 0
    for start, left in enumerate(galaxies, start=1):
        for right in galaxies[start:]:
            dist += left.distance(right)
    
    return dist


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day11.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
