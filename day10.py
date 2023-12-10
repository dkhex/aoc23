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


def make_maze(lines):
    maze = (
        ChainIterable(lines)
            .map(lambda line: "." + line.strip() + ".")
            .collect()
    )
    filler = "." * len(maze[0])
    maze = [filler, *maze, filler]
    return maze


def get_symbol_position(maze, symbol):
    for start_y, row in enumerate(maze):
        start_x = row.find(symbol)
        if start_x >= 0:
            return start_x, start_y
    else:
        raise ValueError(f"Symbol '{symbol}' not found")


def get_connected_pipe(maze, target_pipe):
    for x, y in around_coords(*target_pipe):
        pipe = Pipe(x, y, maze[y][x])
        if pipe.is_connected(target_pipe) and pipe.coords in target_pipe:
            return pipe


def task1(filename):
    with open(filename) as file:
        maze = make_maze(file)
        start_x, start_y = get_symbol_position(maze, "S")
        start_pipe = Pipe(start_x, start_y, "S")
        pipes = [start_pipe]
        pipe = start_pipe
        next_pipe = get_connected_pipe(maze, start_pipe)
        while next_pipe != start_pipe:
            pipes.append(next_pipe)
            x, y = next_pipe.get_next_from(pipe)
            pipe = next_pipe
            next_pipe = Pipe(x, y, maze[y][x])
        return len(pipes) // 2


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day10.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
