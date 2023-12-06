def get_hold_release_times(total_time):
    for hold in range(1, total_time):
        yield hold, (total_time - hold)


def task1(filename):
    data = {}
    with open(filename) as file:
        for line in file:
            name, values = line.split(":")
            data[name] = map(int, values.strip().split())
    races = zip(data["Time"], data["Distance"])
    total_result = 1
    for time, distance in races:
        wins = 0
        for hold, release in get_hold_release_times(time):
            if (hold * release) > distance:
                wins += 1
        total_result *= wins
    return total_result


def task2(filename):
    data = {}
    with open(filename) as file:
        for line in file:
            name, values = line.split(":")
            data[name] = int("".join(values.strip().split()))

    time, distance = data["Time"], data["Distance"]
    wins = 0
    for hold, release in get_hold_release_times(time):
        if (hold * release) > distance:
            wins += 1
    return wins


if __name__ == "__main__":
    filename = "inputs/day6.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
