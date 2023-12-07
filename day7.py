from collections import Counter

from myiters import ChainIterable


strengths_base = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


strengths_joker = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 0,
}


powers = {
    0: lambda _: 7,
    1: lambda _: 7,
    2: lambda c: 6 if c == 4 else 5,
    3: lambda c: 4 if c == 3 else 3,
    4: lambda _: 2,
    5: lambda _: 1,
}


def get_power(cards):
    kinds = Counter(cards)
    return powers[len(kinds)](max(kinds.values()))


def get_power_with_joker(cards):
    kinds = Counter(filter(bool, cards))
    power_func = powers[len(kinds)]
    counts = kinds.values() or [0]
    max_count = max(counts) + cards.count(0)
    return power_func(max_count)


def process_game(hand, bid):
    cards = [strengths_base[card] for card in hand]
    return get_power(cards), cards, int(bid)


def process_game_with_joker(hand, bid):
    cards = [strengths_joker[card] for card in hand]
    return get_power_with_joker(cards), cards, int(bid)


def task1(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(str.split)
                .tuple_map(process_game)
                .sort()
                .enumerate(1)
                .tuple_map(lambda rank, game: rank * game[2])
                .sum()
        )


def task2(filename):
    with open(filename) as file:
        return (
            ChainIterable(file)
                .map(str.split)
                .tuple_map(process_game_with_joker)
                .sort()
                .enumerate(1)
                .tuple_map(lambda rank, game: rank * game[2])
                .sum()
        )


if __name__ == "__main__":
    filename = "inputs/day7.txt"
    print("Task 1:", task1(filename))
    print("Task 2:", task2(filename))
