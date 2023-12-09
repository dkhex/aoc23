from myiters import ChainIterable


def collect_diffs(history):
    result = []
    diff = list(history)
    while True:
        result.append(diff)
        diff = (
            ChainIterable(diff)
                .scan()
                .tuple_map(lambda a, b: b - a)
                .collect()
        )
        if all(d == 0 for d in diff):
            return result


def predict_number(history):
    diffs = collect_diffs(history)
    return (
        ChainIterable(diffs)
            .map(lambda diff: diff[-1])
            .sum()
    )


def task1(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(str.split)
                .submap(int)
                .map(predict_number)
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day9.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
