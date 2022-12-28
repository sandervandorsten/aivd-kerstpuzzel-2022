"""Calculate possible options """
import itertools
from collections import defaultdict
from itertools import combinations, permutations, product

# Create all fields in dartboard
numbers = list(range(1, 21))
singles = {f"S{k}": k for k in numbers}
doubles = {f"D{k}": 2 * k for k in numbers}
triples = {f"T{k}": 3 * k for k in numbers}
bulls = {"B": 25, "DB": 50}
options = singles | doubles | triples | bulls
options_ = list(set(options.values()))

# Create mapping to letters
letters = {
    "S1": "C",
    "S2": "A",
    "S3": "N",
    "S4": "O",
    "S5": "P",
    "S6": "U",
    "S7": "S",
    "S8": "E",
    "S9": "W",
    "S10": "K",
    "S11": "P",
    "S12": "Z",
    "S13": "N",
    "S14": "S",
    "S15": "R",
    "S16": "G",
    "S17": "P",
    "S18": "J",
    "S19": "W",
    "S20": "T",
    "D1": "T",
    "D2": "P",
    "D3": "L",
    "D4": "R",
    "D5": "A",
    "D6": "Y",
    "D7": "O",
    "D8": "B",
    "D9": "A",
    "D10": "N",
    "D11": "O",
    "D12": "P",
    "D13": "E",
    "D14": "N",
    "D15": "A",
    "D16": "N",
    "D17": "O",
    "D18": "E",
    "D19": "E",
    "D20": "R",
    "T1": "A",
    "T2": "R",
    "T3": "M",
    "T4": "H",
    "T5": "N",
    "T6": "D",
    "T7": "D",
    "T8": "F",
    "T9": "U",
    "T10": "I",
    "T11": "M",
    "T12": "A",
    "T13": "A",
    "T14": "O",
    "T15": "C",
    "T16": "L",
    "T17": "I",
    "T18": "E",
    "T19": "O",
    "T20": "H",
    "B": "S",
    "DB": "T",
}


# invert all options (based on score) and sort descending
score_dict = defaultdict(list)
for key, val in sorted(options.items()):
    score_dict[val].append(key)
score_list = tuple(sorted(score_dict.items(), key=lambda x: x[0], reverse=True))


def calc(dart_throw: int, number_options: list[int, list[str]]) -> list[int]:
    """Calculate denominator"""
    left_over = dart_throw
    darts = []
    while len(darts) < 3:
        for number, opt in number_options:
            if left_over - number > 0:
                darts.append(opt)


# def get_combinations_old(
#     value: int,
#     character_length: list[int] = [1, 2, 3],
# ) -> list[tuple[int]]:
#     result = []
#     for i in character_length:
#         possible_combination = list(combinations(options_, i))
#         result.append([each for each in possible_combination if sum(each) == value])
#     return list(itertools.chain(*result))


def get_combinations(
    value: int,
    character_length: list[int] = [1, 2, 3],
) -> list[list[int]]:
    result = []
    for i in character_length:
        possible_combination = list(combinations(options_, i))
        result.append([each for each in possible_combination if sum(each) == value])
    return [sorted(option, reverse=True) for option in tuple(itertools.chain(*result))]


# def number_combis_to_dart_names(number_combi: list[tuple[int]]) -> list[list[str]]:
#     """Convert number combi's in all options
#     TODO: only grabs the first one now
#     """
#     return [[score_dict[d][0] for d in option] for option in number_combi]
#


def number_combis_to_dart_names_new(
    number_combi: list[list[int]],
    last_dart: bool = False,
) -> list[tuple[str]]:
    """Convert number combi's in all options"""
    nested_result = [[score_dict[d] for d in option] for option in number_combi]
    flat_result = list(itertools.chain(*[product(*x) for x in nested_result]))
    if last_dart:
        flat_result = [
            option for option in flat_result if any(["D" in dart for dart in option])
        ]
    return flat_result


def dart_names_to_letters(dart_names: list[tuple[str]]):
    return [[letters[dart] for dart in option] for option in dart_names]


def process_one(number: int, last_dart: bool = False):
    x = get_combinations(number)
    y = number_combis_to_dart_names_new(x, last_dart=last_dart)
    z = dart_names_to_letters(y)
    r = ["".join(char) for option in z for char in list(permutations(option))]
    return r


def process_multi(numbers: list[int]):
    x = [process_one(n) for n in numbers[:-1]] + [
        process_one(numbers[-1], last_dart=True)
    ]
    y = ["".join(x) for x in product(*x)]
    return y
