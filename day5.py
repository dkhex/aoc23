class Mapper:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.mappings = []

    def add_mapping(self, mapping_string):
        dst, src, cnt = map(int, mapping_string.split())
        self.mappings.append((range(src, src + cnt), dst - src))

    def map_values(self, values):
        for value in values:
            for mapping_range, offset in self.mappings:
                if value in mapping_range:
                    yield value + offset
                    break
            else:
                yield value


def task1(filename):
    numbers = []
    mappers = {}
    mapper = None
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                name, rest = line.split(":")
                if name == "seeds":
                    numbers = list(map(int, rest.strip().split()))
                else:
                    name, _ = name.split()
                    src, dst = name.split("-to-")
                    mapper = Mapper(src, dst)
                    mappers[mapper.source] = mapper
            else:
                mapper.add_mapping(line)
    source = "seed"
    while source != "location":
        mapper = mappers[source]
        numbers = list(mapper.map_values(numbers))
        source = mapper.destination
    return min(numbers)


def task2(filename):
    with open(filename) as file:
        ...


if __name__ == "__main__":
    filename = "inputs/day5.txt"
    print("Task 1:", task1(filename))
    # print("Task 2:", task2(filename))
