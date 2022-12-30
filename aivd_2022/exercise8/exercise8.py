"""Calculate possible options """
import itertools
from collections import defaultdict
from itertools import permutations, product, combinations_with_replacement
import pandas as pd
import datetime as dt

# Create all fields in dartboard
numbers = list(range(1, 21))
singles = {f"S{k}": k for k in numbers}
doubles = {f"D{k}": 2 * k for k in numbers}
triples = {f"T{k}": 3 * k for k in numbers}
bulls = {"B": 25, "DB": 50}
dart_value_mapping = singles | doubles | triples | bulls
unique_dart_values = list(set(dart_value_mapping.values()))

last_dart_values = list(doubles.values()) + [bulls["DB"]]

# Create mapping to letters
dart2letters = {
    "S1": "C",
    "S2": "A/E",
    "S3": "N/T",
    "S4": "O",
    "S5": "P/C",
    "S6": "U/E",
    "S7": "S/L",
    "S8": "E/C",
    "S9": "W/T",
    "S10": "K/V",
    "S11": "P/G",
    "S12": "Z/X",
    "S13": "N/A",
    "S14": "S/U",
    "S15": "R",
    "S16": "G/O",
    "S17": "P/B",
    "S18": "J/H",
    "S19": "W/F",
    "S20": "T/Y",
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

# mapping: with how many throws can you throw which numbers?
# highest values first
dart_throw_combis: dict[int, list[list[int, ...]]] = {
    i: sorted(
        [
            sorted(combi, reverse=True)
            for combi in combinations_with_replacement(unique_dart_values, i)
        ],
        reverse=True,
    )
    for i in range(4)
}


def invert_dict(d: dict[str, int]) -> dict[int, list[str]]:
    """Invert dict. create list for non-unique keys."""
    d_inverted = defaultdict(list)
    for key, val in sorted(d.items()):
        d_inverted[val].append(key)
    return d_inverted


# invert all options (based on score) and sort descending
dart_value_mapping_inverted = invert_dict(dart_value_mapping)
dart_value_mapping_inv_tuple = tuple(
    sorted(dart_value_mapping_inverted.items(), key=lambda x: x[0], reverse=True)
)


def get_combinations(
    value: int,
    last_dart: bool = False,
) -> list[list[int]]:
    """Retrieve all possible number combinations for getting 'value'."""
    n_darts = [1, 2, 3] if last_dart else [3]
    result = [
        each for i in n_darts for each in dart_throw_combis[i] if sum(each) == value
    ]

    if last_dart:
        # create all permutations...
        result = list(itertools.chain(*[permutations(option) for option in result]))
        # Only keep result where last dart is a final dart
        result = [option for option in result if option[-1] in last_dart_values]
        # keep only 1 option per combination to stay more consise
        unique_combis = [
            set(option) for option in set([tuple(sorted(option)) for option in result])
        ]
        results_with_final_dart = []
        for option in sorted(result, reverse=True):
            if set(option) in unique_combis:
                results_with_final_dart.append(option)
                unique_combis.remove(set(option))
        return results_with_final_dart
    return result


def number_combi_to_dart_names(
    number_combi: list[int], last_dart: bool = False
) -> list[str]:

    result = list(
        itertools.chain(
            *[product(*[dart_value_mapping_inverted[d] for d in number_combi])]
        )
    )
    # Keep only results with doubles
    # make sure dart is last
    if last_dart:
        result = [option for option in result if any(["D" in dart for dart in option])]
    else:
        new_result = []
        for option in result:
            if len(option) == 3:
                new_result.append(option)
            else:
                if any(["D" in dart for dart in option]):
                    new_result.append(option)

    return result


def number_combi_list_to_dart_names(
    number_combi_list: list[list[int]],
    last_dart: bool = False,
) -> list[tuple[str]]:
    """Convert number combi's in all options"""
    result = list(
        itertools.chain(
            *[
                number_combi_to_dart_names(number_combi, last_dart=last_dart)
                for number_combi in number_combi_list
            ]
        )
    )
    return result


def dart_names_to_letters(dart_names: tuple[str]) -> list[str]:
    return [dart2letters[dart] for dart in dart_names]


def dart_names_list_to_letters(dart_names: list[tuple[str]]) -> list[list[str]]:
    return [dart_names_to_letters(option) for option in dart_names]


def process_one(
    number: int, last_dart: bool = False
) -> tuple[list[tuple[str]], list[str]]:
    number_combis = get_combinations(number, last_dart=last_dart)
    dart_names = number_combi_list_to_dart_names(number_combis, last_dart=last_dart)
    letters = dart_names_list_to_letters(dart_names)
    words = ["".join(option) for option in letters]
    return dart_names, words


def process_multi(numbers: list[int]):
    dart_names_list = []
    words_list = []
    for i, n in enumerate(numbers, start=1):
        last_dart = True if i == len(numbers) else False
        dart_names, words = process_one(n, last_dart=last_dart)
        dart_names_list.append(dart_names)
        words_list.append(words)

    return dart_names_list, words_list


def export(
    numbers: list[int],
    dart_names_list: list[list[tuple[str]]],
    words_list: list[list[str]],
):
    now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    words_df = pd.DataFrame(data=words_list, index=numbers).T
    dart_names_df = pd.DataFrame(data=dart_names_list, index=numbers).T

    with pd.ExcelWriter(f"export/{numbers}-{now}.xlsx") as writer:
        words_df.to_excel(writer, sheet_name="words_df")
        dart_names_df.to_excel(writer, sheet_name="dart_names_df")


def main():
    number_sets = [
        [167, 167, 167],
        [128, 126, 164, 75, 8],
        [93, 125, 112, 131, 10, 18, 12],
        [96, 19, 150, 66, 144, 26],
    ]
    for numbers in number_sets:
        dart_names_list, words_list = process_multi(numbers)
        export(numbers, dart_names_list, words_list)


if __name__ == "__main__":
    main()
