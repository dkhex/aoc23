from myiters import ChainIterable


def match_damaged_counts(record, counts):
    c = 0
    res = []
    for template in record:
        damaged = []
        count = -1
        while (c < len(counts)) and (count + counts[c] + 1) <= len(template):
            damaged.append(counts[c])
            count += counts[c] + 1
            c += 1
        res.append((template, damaged))
    return res


def task1(filename):
    with open(filename) as file:
        data = (
            ChainIterable(file)
                .map(str.split)
                .tuple_map(
                    lambda record, counts: (
                        record.replace(".", " ").split(),
                        [int(c) for c in counts.split(",")],
                    )
                )
                .tuple_map(match_damaged_counts)
                .flat()
                .collect()
        )
    return data


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day12.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
