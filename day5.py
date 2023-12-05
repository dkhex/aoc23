class NumbersRange:
    def __init__(self, start, count=None, end=None):
        if count is None and end is None:
            raise ValueError("Can't initialize without one of arguments")
        if count is None:
            if end < start:
                raise ValueError("`end` should be greater than `start`")
            count = end - start
        if end is None:
            end = start + count
        self.start = start
        self.end = end
        self.count = count

    def __contains__(self, number):
        return self.start <= number < self.end

    def offset(self, offset):
        return NumbersRange(start=self.start + offset, count=self.count)

    def intersection(self, other):
        second_start = max(self.start, other.start)
        first_end = min(self.end, other.end)
        if first_end > second_start:
            yield NumbersRange(start=second_start, end=first_end)

    def cut(self, other):
        start, end = self.start, min(self.end, other.start)
        if end > start:
            yield NumbersRange(start=start, end=end)
        start, end = max(self.start, other.end), self.end
        if end > start:
            yield NumbersRange(start=start, end=end)


class Mapper:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.mappings = []

    def add_mapping(self, mapping_string):
        dst, src, cnt = map(int, mapping_string.split())
        self.mappings.append((NumbersRange(start=src, count=cnt), dst - src))

    def map_values(self, values):
        for value in values:
            for mapping_range, offset in self.mappings:
                if value in mapping_range:
                    yield value + offset
                    break
            else:
                yield value

    def map_ranges(self, ranges):
        for rng in ranges:
            group = [rng]
            for mapping_range, offset in self.mappings:
                for r in group:
                    for intersection in r.intersection(mapping_range):
                        yield intersection.offset(offset)
                    group = list(r.cut(mapping_range))
            for r in group:
                yield r


def get_info(lines):
    source = None
    numbers = None
    mappers = {}
    mapper = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            name, rest = line.split(":")
            if rest:
                source = name
                numbers = list(map(int, rest.strip().split()))
            else:
                name, _ = name.split()
                src, dst = name.split("-to-")
                mapper = Mapper(src, dst)
                mappers[mapper.source] = mapper
        else:
            mapper.add_mapping(line)

    if source is None or numbers is None:
        raise ValueError("File missing starting sequence")

    if source not in mappers:
        source = source[:-1]
        if source not in mappers:
            raise ValueError("File missing mapper for starting sequence")

    for mapper in mappers.values():
        if mapper.destination not in mappers:
            destination = mapper.destination

    return source, destination, numbers, mappers


def task1(filename):
    with open(filename) as file:
        source, destination, numbers, mappers = get_info(file)

    while source != destination:
        mapper = mappers[source]
        numbers = list(mapper.map_values(numbers))
        source = mapper.destination

    return min(numbers)


def task2(filename):
    with open(filename) as file:
        source, destination, numbers, mappers = get_info(file)

    ranges = [NumbersRange(start=numbers[i], count=numbers[i+1]) for i in range(0, len(numbers), 2)]

    while source != destination:
        mapper = mappers[source]
        ranges = list(mapper.map_ranges(ranges))
        source = mapper.destination

    return min(ranges, key=lambda r: r.start).start


if __name__ == "__main__":
    filename = "inputs/day5.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
