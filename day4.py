from collections import defaultdict

from myiters import ChainIterable


def get_win_counts(lines):
    return (
        ChainIterable(lines)
            .map(lambda line: line.split(":")[-1].strip())
            .map(lambda line: line.split("|"))
            .submap(str.split)
            .submap(set)
            .tuple_map(set.intersection)
            .map(len)
    )


def task1(filename):
    with open(filename) as file:
        return (
            get_win_counts(file)
                .map(lambda count: (1 << count) // 2)
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        win_counts = get_win_counts(file).collect()

    copy_counts = defaultdict(lambda: 1)
    for next_number, wins in enumerate(win_counts, start=1):
        for card_number in range(next_number, next_number + wins):
            copy_counts[card_number] += copy_counts[next_number - 1]
    return sum(copy_counts.values())


if __name__ == "__main__":
    filename = "inputs/day4.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
