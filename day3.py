class Number:
    def __init__(self, value):
        self.value = value


def around_coords(x, y):
    yield (x - 1, y - 1)
    yield (x    , y - 1)
    yield (x + 1, y - 1)
    yield (x - 1, y    )
    #     (x    , y    )
    yield (x + 1, y    )
    yield (x - 1, y + 1)
    yield (x    , y + 1)
    yield (x + 1, y + 1)


def get_numbers_and_symbols(row_string):
    numbers = {}
    symbols = []
    num = 0
    is_num = False
    start = 0
    for i, s in enumerate(row_string, start=1):
        if s.isdigit():
            num *= 10
            num += int(s)
            if not is_num:
                start = i
                is_num = True
        else:
            if is_num:
                is_num = False
                number = Number(num)
                numbers.update({n: number for n in range(start, i)})
                num = 0
            if s != ".":
                symbols.append((i, s))
    return numbers, symbols


def process_rows(lines):
    number_rows = [{}]
    symbol_rows = [[]]
    for line in lines:
        numbers, symbols = get_numbers_and_symbols(line.replace("\n", "."))
        number_rows.append(numbers)
        symbol_rows.append(symbols)
    number_rows.append({})
    symbol_rows.append([])
    return number_rows, symbol_rows


def task1(filename):
    with open(filename) as file:
        number_rows, symbol_rows = process_rows(file)

    number_set = set()
    for row_num, row in enumerate(symbol_rows):
        for symbol_pos, _ in row:
            for x, y in around_coords(symbol_pos, row_num):
                if (number := number_rows[y].get(x)) is not None:
                    number_set.add(number)

    return sum(map(lambda x: x.value, number_set))


def task2(filename):
    with open(filename) as file:
        number_rows, symbol_rows = process_rows(file)

    ratios = []
    for row_num, row in enumerate(symbol_rows):
        for symbol_pos, symbol in row:
            if symbol != "*":
                continue
            adjacent = set()
            for x, y in around_coords(symbol_pos, row_num):
                if (number := number_rows[y].get(x)) is not None:
                    adjacent.add(number)
            if len(adjacent) == 2:
                a, b = adjacent
                ratios.append(a.value * b.value)

    return sum(ratios)


if __name__ == "__main__":
    filename = "inputs/day3.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
