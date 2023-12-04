from myiters import ChainIterable


def task1(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(lambda line: line.split(":")[-1].strip())
                .map(lambda line: line.split("|"))
                .submap(str.split)
                .submap(set)
                .tuple_map(set.intersection)
                .map(len)
                .map(lambda count: (1 << count) // 2)
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day4.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
