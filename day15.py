def get_hash(label):
    label_hash = 0
    for char in label:
        label_hash += ord(char)
        label_hash *= 17
    label_hash %= 256
    return label_hash


def get_boxes_powers(boxes):
    for box_number, lenses in enumerate(boxes, start=1):
        for lens_num, focal in enumerate(lenses.values(), start=1):
            yield box_number * lens_num * focal


def task1(filename):
    with open(filename) as file:
        sequence = file.read().strip().split(",")

    return sum(map(get_hash, sequence))


def task2(filename):
    with open(filename) as file:
        sequence = file.read().strip().split(",")

    boxes = [{} for _ in range(256)]

    for step in sequence:
        if "-" in step:
            label = step[:step.find("-")]
            label_hash = get_hash(label)
            if label in boxes[label_hash]:
                del boxes[label_hash][label]
        elif "=" in step:
            label = step[:step.find("=")]
            label_hash = get_hash(label)
            value = int(step[-1])
            boxes[label_hash][label] = value

    return sum(get_boxes_powers(boxes))


if __name__ == "__main__":
    filename = "inputs/day15.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
