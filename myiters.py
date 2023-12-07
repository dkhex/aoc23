from functools import wraps


def scan(iterable, window=2):
    it = iter(iterable)
    try:
        elems = [next(it) for _ in range(window)]
    except StopIteration:
        return
    yield elems
    for e in it:
        _, *elems = *elems, e
        yield elems


def tuple_map(func, iterable):
    for tup in iterable:
        yield func(*tup)


def flat_map(func, iterable):
    for tup in iterable:
        result = func(*tup)
        for elem in result:
            yield elem


def take(iterable, num):
    for _, elem in zip(range(num), iterable):
        yield elem


class ChainUnit:
    def __init__(self, wrapper, name):
        self.wrapper = wrapper
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.name}>"

    def __call__(self, it):
        return self.wrapper(it)


def chain_unit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        unit_wrapper = method(self, *args, **kwargs)
        unit = ChainUnit(unit_wrapper, method.__name__)
        return ChainIterable(self.iterable, self.chain + [unit])
    return wrapper


class ChainIterable:
    def __init__(self, iterable, chain=None):
        if isinstance(iterable, ChainIterable):
            self.iterable = iterable.iterable
            self.chain = iterable.chain + (chain or [])
        else:
            self.iterable = iterable
            self.chain = chain or []

    def __iter__(self):
        it = iter(self.iterable)
        for unit in self.chain:
            it = unit(it)
        return it

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self.iterable!r} with {self.chain}>"

    @chain_unit
    def map(self, func):
        return lambda x: map(func, x)

    @chain_unit
    def submap(self, func):
        return lambda x: map(lambda e: map(func, e), x)

    @chain_unit
    def tuple_map(self, func):
        return lambda x: tuple_map(func, x)

    @chain_unit
    def flat_map(self, func):
        return lambda x: flat_map(func, x)

    @chain_unit
    def filter(self, pred=lambda x: x is not None):
        return lambda x: filter(pred, x)

    @chain_unit
    def subfilter(self, pred=lambda x: x is not None):
        return lambda x: map(lambda e: filter(pred, e), x)

    @chain_unit
    def scan(self, window: int=2):
        return lambda x: scan(x, window)

    @chain_unit
    def take(self, num: int):
        return lambda x: take(x, num)

    @chain_unit
    def zip(self, *iterables):
        return lambda x: zip(x, *iterables)

    @chain_unit
    def enumerate(self, start=0):
        return lambda x: enumerate(x, start=start)

    def sort(self, key=None):
        return ChainIterable(sorted(self, key=key))

    def sorted(self, key=None):
        return sorted(self, key=key)

    def collect(self):
        return list(self)

    def sum(self):
        return sum(self)

    def any(self, pred=None):
        if pred is None:
            return any(self)
        else:
            return any(self.map(pred))

    def all(self, pred=None):
        if pred is None:
            return all(self)
        else:
            return all(self.map(pred))


def chain_zip(*iterables):
    return ChainIterable(zip(*iterables))
