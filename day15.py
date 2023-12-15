def task1(filename):
    with open(filename) as file:
        sequence = file.read().strip().split(",")

    hash_sum = 0
    for step in sequence:
        step_hash = 0
        for char in step:
            step_hash += ord(char)
            step_hash *= 17
        step_hash %= 256
        hash_sum += step_hash

    return hash_sum


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day15.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
