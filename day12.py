from myiters import ChainIterable


def get_arrangements_count(template, counts):
    if not counts:
        return 1

    if not "?" in template:
        if len(counts) != 1 or counts[0] != len(template):
            raise ValueError("Something is wrong")
        return 1

    indexes = (
        ChainIterable(template)
            .enumerate()
            .tuple_filter(lambda i, s: s == "?")
            .tuple_map(lambda i, s: i)
            .collect()
    )

    arrangements = 0

    for mut in range(1 << (len(indexes))):
        cnts = []
        value = 0

        for i in range(len(template)):
            if i in indexes:
                if mut & 1:
                    value += 1
                elif value:
                    cnts.append(value)
                    value = 0
                mut >>= 1
            else:
                if template[i] == "#":
                    value += 1
                elif value:
                    cnts.append(value)
                    value = 0

        if value:
            cnts.append(value)

        if cnts == counts:
            arrangements += 1

    return arrangements


def task1(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(str.split)
                .tuple_map(
                    lambda record, counts: (
                        record,
                        [int(c) for c in counts.split(",")],
                    )
                )
                .tuple_map(get_arrangements_count)
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day12.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
