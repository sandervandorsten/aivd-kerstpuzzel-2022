from pathlib import Path
import json
from exercise11 import expand_solutions, add_final_words, add_missing_data, export


def import_jsonlines(filename: Path) -> list[dict[str, str]]:
    with open(str(filename), "r") as f:
        lines: list[str] = f.readlines()
        solutions = [json.loads(line) for line in lines]
    return solutions


def main():
    path = Path("./export/20221229-224442-LINGO_MWB_WORDFEUD-abcdefg.jsonlines")
    split_filename = path.stem.split("-")
    columns = list(split_filename[-1])
    corpora = split_filename[-2].split("_")
    solutions = import_jsonlines(path)
    words, cols_with_data = expand_solutions(solutions, columns)

    words = add_missing_data(words, columns, cols_with_data)
    words = add_final_words(words, columns)
    export(words, cols_with_data, corpora)


if __name__ == "__main__":
    main()
