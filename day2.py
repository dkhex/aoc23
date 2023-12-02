from functools import reduce
from operator import mul


colors = {"red": 12, "green": 13, "blue": 14}


def get_maximums(sets_string):
    maximums = {c: 0 for c in colors}
    pair_strings = sets_string.replace(";", ",").split(",")
    for count, name in map(str.split, pair_strings):
        maximums[name] = max(maximums[name], int(count))
    return maximums


def get_id_if_ok(game_string):
    number_string, sets_string = game_string.split(":")
    number = int(number_string.split()[-1])
    maximums = get_maximums(sets_string)
    for color, value in maximums.items():
        if value > colors[color]:
            return 0
    return number


def get_power(game_string):
    _, sets_string = game_string.split(":")
    maximums = get_maximums(sets_string)
    return reduce(mul, maximums.values())


def task1(filename):
    with open(filename) as file:
        return sum(map(get_id_if_ok, file))


def task2(filename):
    with open(filename) as file:
        return sum(map(get_power, file))


if __name__ == "__main__":
    filename = "inputs/day2.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
