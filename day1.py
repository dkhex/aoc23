from myiters import ChainIterable


digits_map = {
    "one":   1,
    "two":   2,
    "three": 3,
    "four":  4,
    "five":  5,
    "six":   6,
    "seven": 7,
    "eight": 8,
    "nine":  9,
}


def digits_extract(line):
    for idx, char in enumerate(line):
        if char.isdigit():
            yield int(char)
        else:
            for name, digit in digits_map.items():
                if line[idx:].startswith(name):
                    yield digit
                    break


def task1(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .subfilter(str.isdigit)
                .submap(int)
                .map(list)
                .filter(bool)
                .map(lambda digits: digits[0] * 10 + digits[-1])
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(digits_extract)
                .map(list)
                .filter(bool)
                .map(lambda digits: digits[0] * 10 + digits[-1])
                .sum()
        )


if __name__ == "__main__":
    filename = "inputs/day1.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
