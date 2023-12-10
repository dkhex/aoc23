from myiters import ChainIterable


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
                .map(Pipe.coords.fget)
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


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day10.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
