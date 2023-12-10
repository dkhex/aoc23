from myiters import ChainIterable


circle = [
    ( 0, -1),
    (+1, -1),
    (+1,  0),
    (+1, +1),
    ( 0, +1),
    (-1, +1),
    (-1,  0),
    (-1, -1),
]
double_circle = circle + circle


def around_coords(x, y):
    yield (x    , y - 1)
    yield (x + 1, y    )
    yield (x    , y + 1)
    yield (x - 1, y    )


class Pipe:
    symbols = {
        "|": (( 0, -1), ( 0, +1)),
        "-": ((-1,  0), (+1,  0)),
        "L": (( 0, -1), (+1,  0)),
        "J": (( 0, -1), (-1,  0)),
        "7": (( 0, +1), (-1,  0)),
        "F": (( 0, +1), (+1,  0)),
        ".": (( 0,  0), ( 0,  0)),
        "S": (( 0, -1), (+1,  0), ( 0, +1), (-1,  0)),
    }

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        connections = self.symbols[symbol]
        self.connections = [(self.x + conn_x, self.y + conn_y) for conn_x, conn_y in connections]

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other) -> bool:
        return (self.x, self.y) == other

    def __contains__(self, other):
        return other in self.connections

    @property
    def coords(self):
        return (self.x, self.y)

    def get_coords(self):
        return self.coords

    def get_next_from(self, other_pipe):
        for conn in self.connections:
            if conn != other_pipe.coords:
                return conn

    def is_connected(self, other_pipe):
        return any(conn == other_pipe for conn in self.connections)


class Maze:
    def __init__(self, lines):
        maze = (
            ChainIterable(lines)
                .map(lambda line: "." + line.strip() + ".")
                .collect()
        )
        filler = "." * len(maze[0])
        self.maze = [filler, *maze, filler]

    def __iter__(self):
        return iter(self.maze)

    def get_pipe(self, x, y):
        return Pipe(x, y, self.maze[y][x])

    def get_start_pipe(self, start_symbol):
        for start_y, row in enumerate(self):
            start_x = row.find(start_symbol)
            if start_x >= 0:
                break
        else:
            raise ValueError(f"Symbol '{start_symbol}' not found")

        start_pipe = self.get_pipe(start_x, start_y)

        start_pipe.connections = (
            ChainIterable(start_pipe.connections)
                .tuple_map(self.get_pipe)
                .filter(lambda pipe: pipe.is_connected(start_pipe))
                .map(Pipe.get_coords)
                .collect()
        )

        return start_pipe

    def get_loop(self, start_pipe):
        loop = [start_pipe]
        pipe = start_pipe
        next_pipe = self.get_pipe(*start_pipe.connections[0])

        while next_pipe != start_pipe:
            loop.append(next_pipe)
            x, y = next_pipe.get_next_from(pipe)
            pipe = next_pipe
            next_pipe = self.get_pipe(x, y)

        return loop


def task1(filename):
    with open(filename) as file:
        maze = Maze(file)

    start_pipe = maze.get_start_pipe("S")
    loop = maze.get_loop(start_pipe)
    return len(loop) // 2


def group_tiles(prev, curr, next):
    rel_prev = prev[0] - curr[0], prev[1] - curr[1]
    rel_next = next[0] - curr[0], next[1] - curr[1]
    prev_index = circle.index(rel_prev)
    next_index = circle.index(rel_next)
    next_inc = (next_index < prev_index) * 8
    prev_inc = (not next_inc) * 8
    left_offsets = double_circle[prev_index + 1 : next_index + next_inc]
    right_offsets = double_circle[next_index + 1 : prev_index + prev_inc]
    left = set((curr[0] + x, curr[1] + y) for x, y in left_offsets)
    right = set((curr[0] + x, curr[1] + y) for x, y in right_offsets)
    return left, right


### DEBUG
# def visualize_sets(loop, left, right):
#     temp = [[" " for _ in range(142)] for _ in range(142)]
#     for x, y in loop:
#         temp[y][x] = "+"
#     for x, y in left:
#         temp[y][x] = "L"
#     for x, y in right:
#         temp[y][x] = "R"
#     with open("out.txt", "w") as file:
#         for line in temp:
#             file.write("".join(line) + "\n")


def task2(filename):
    with open(filename) as file:
        maze = Maze(file)

    start_pipe = maze.get_start_pipe("S")
    loop = maze.get_loop(start_pipe)
    loop_set = set(pipe.coords for pipe in loop)

    by_groups = (
        ChainIterable(loop + loop[:2])
            .map(Pipe.get_coords)
            .scan(3)
            .tuple_map(group_tiles)
    )
    left_set = set()
    right_set = set()

    for left, right in by_groups:
        left_set |= left - loop_set
        right_set |= right - loop_set

    row = start_pipe.coords[1]
    for col in range(start_pipe.coords[1]):
        if (col, row) in left_set:
            new_set = right_set
            break
        if (col, row) in right_set:
            new_set = left_set
            break

    ### DEBUG
    # visualize_sets(loop_set, left_set, right_set)

    inner_set = set()
    while new_set:
        inner_set |= new_set
        collected = set()
        for x, y in new_set:
            for coord in around_coords(x, y):
                if coord not in inner_set and coord not in loop_set:
                    collected.add(coord)
        new_set = collected

    return len(inner_set)


if __name__ == "__main__":
    filename = "inputs/day10.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
