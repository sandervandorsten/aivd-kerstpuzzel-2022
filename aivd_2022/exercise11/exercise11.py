import json

from constraint import *
import string
from preprocess_data import retrieve_corpus
import pandas as pd
import datetime as dt


def in_corpus(x1, x2, x3, x4, x5, corpus):
    """Checks if a word is in the corpus"""
    return x1 + x2 + x3 + x4 + x5 in corpus


def csp(corpus, corpora: list[str], vars: list[str], iterative: bool = False):
    start_time = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    corpora_str = "_".join(corpora)

    # word subsets
    z = list(set([word[0] for word in corpus]))
    w = list(set([word[1] for word in corpus]))
    k = list(set([word[2] for word in corpus]))
    y = list(set([word[3] for word in corpus]))
    x = list(set([word[4] for word in corpus]))
    yw = list(set(y + w))
    alphabet = list(string.ascii_lowercase)

    # Problem definition.
    problem = Problem()

    def add_a():
        print("Adding A...")
        problem.addVariable("a1", z)
        problem.addVariable("a2", w)
        problem.addVariable("a3", k)
        problem.addVariable("a4", y)
        problem.addVariable("a5", x)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("a1", "a2", "a3", "a4", "a5"),
        )

    def add_b():
        print("Adding B...")
        # B
        problem.addVariable("b1", k)
        problem.addVariable("b2", alphabet)
        problem.addVariable("b3", alphabet)
        problem.addVariable("b4", y)
        problem.addVariable("b5", x)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("b1", "b2", "b3", "b4", "b5"),
        )
        # Geen Z op 1
        problem.addConstraint(
            lambda x1, var: (x1 != var),
            ("b1", "a1"),
        )
        # Geen W op 2
        problem.addConstraint(
            lambda x1, var: (x1 != var),
            ("b2", "a2"),
        )
        # Geen K op 3
        problem.addConstraint(
            lambda x1, var: (x1 != var),
            ("b3", "a3"),
        )

        # K
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a3", "b1"),
        )

        # X
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a5", "b5"),
        )

        # Y
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a4", "b4"),
        )

    def add_c():
        print("Adding C...")
        problem.addVariable("c1", x)
        problem.addVariable("c2", alphabet)
        problem.addVariable("c3", k)
        problem.addVariable("c4", alphabet)
        problem.addVariable("c5", k)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("c1", "c2", "c3", "c4", "c5"),
        )

        # Geen Y in C4
        problem.addConstraint(
            lambda x1, var: (x1 != var),
            ("c4", "a4"),
        )

        # Alpha != Omega
        problem.addConstraint(
            lambda x1, x2: x1 != x2,
            ("b2", "c2"),
        )

        # K
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a3", "c3"),
        )
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a3", "c5"),
        )

        # X
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a5", "c1"),
        )

    def add_d():
        print("Adding D...")

        # D
        problem.addVariable("d1", alphabet)
        problem.addVariable("d2", alphabet)
        problem.addVariable("d3", alphabet)
        problem.addVariable("d4", k)
        problem.addVariable("d5", k)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("d1", "d2", "d3", "d4", "d5"),
        )

        # D1 is no X or K
        problem.addConstraint(
            lambda x1, var, var2: (x1 != var) & (x1 != var2),
            ("d1", "a5", "a3"),
        )

        # D3 is no K or Z
        problem.addConstraint(
            lambda x1, var, var2: (x1 != var) & (x1 != var2),
            ("d3", "a3", "a1"),
        )

        # Alpha
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("d2", "c2"),
        )

        # K
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("d4", "a3"),
        )

        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("d5", "a3"),
        )

    def add_e():
        print("Adding E...")

        # E
        problem.addVariable("e1", k)
        problem.addVariable("e2", alphabet)
        problem.addVariable("e3", z)
        problem.addVariable("e4", k)
        problem.addVariable("e5", yw)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("e1", "e2", "e3", "e4", "e5"),
        )

        # No Alpha or K in E2
        problem.addConstraint(
            lambda x1, var, var2: (x1 != var) & (x1 != var2),
            ("e2", "c2", "a3"),
        )

        # No X in E
        # TODO deduced/infered, not directly written down as rule.
        # problem.addConstraint(
        #     lambda x1, x2, x3, x4, x5, var: (
        #         (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
        #     ),
        #     ("e1", "e2", "e3", "e4", "e5", "a5"),
        # )

        # K
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("e1", "a3"),
        )

        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("e4", "a3"),
        )

        # Z
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("e3", "a1"),
        )

        # Y or W
        problem.addConstraint(
            lambda x1, x2, x3: x1 == x2 or x1 == x3,
            ("e5", "a2", "a4"),
        )

    def add_f():
        print("Adding F...")

        # F
        problem.addVariable("f1", yw)
        problem.addVariable("f2", alphabet)
        problem.addVariable("f3", yw)
        problem.addVariable("f4", alphabet)
        problem.addVariable("f5", x)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("f1", "f2", "f3", "f4", "f5"),
        )

        # No Z in F
        problem.addConstraint(
            lambda x1, x2, x3, x4, x5, var: (
                (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
            ),
            ("f1", "f2", "f3", "f4", "f5", "a1"),
        )

        # No K in F
        problem.addConstraint(
            lambda x1, x2, x3, x4, x5, var: (
                (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
            ),
            ("f1", "f2", "f3", "f4", "f5", "a3"),
        )

        # No Alpha in F
        problem.addConstraint(
            lambda x1, x2, x3, x4, x5, var: (
                (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
            ),
            ("f1", "f2", "f3", "f4", "f5", "c2"),
        )

        # Y or W
        problem.addConstraint(
            lambda x1, x2, x3: x1 == x2 or x1 == x3,
            ("f1", "a2", "a4"),
        )
        problem.addConstraint(
            lambda x1, x2, x3: x1 == x2 or x1 == x3,
            ("f3", "a2", "a4"),
        )

        # X
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a5", "f5"),
        )

        # Contains a Y
        problem.addConstraint(
            lambda x1, x2, var: ((x1 == var) or (x2 == var)),
            ("f1", "f3", "a4"),
        )

        # Contains a W
        problem.addConstraint(
            lambda x1, x2, var: ((x1 == var) or (x2 == var)),
            ("f1", "f3", "a2"),
        )

    def add_g():
        print("Adding G...")

        problem.addVariable("g1", z)
        problem.addVariable("g2", k)
        problem.addVariable("g3", alphabet)
        problem.addVariable("g4", alphabet)
        problem.addVariable("g5", alphabet)

        problem.addConstraint(
            lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5, corpus),
            ("g1", "g2", "g3", "g4", "g5"),
        )

        # No X in G
        # valid, because we can infer using Worldle 6(F) inference.
        problem.addConstraint(
            lambda x1, x2, x3, x4, x5, var: (
                (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
            ),
            ("g1", "g2", "g3", "g4", "g5", "a5"),
        )

        # No Y in G
        # valid, because we can infer using Worldle 6(F) inference.
        problem.addConstraint(
            lambda x1, x2, x3, x4, x5, var: (
                (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
            ),
            ("g1", "g2", "g3", "g4", "g5", "a4"),
        )

        # Only 1K in G, so not on G4 and G5
        problem.addConstraint(
            lambda x1, x2, var: ((x1 != var) & (x2 != var)),
            ("g4", "g5", "a3"),
        )

        # Z
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a1", "g1"),
        )

        # K
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("a3", "g2"),
        )

        # Alpha
        problem.addConstraint(
            lambda x1, x2: x1 == x2,
            ("c2", "g3"),
        )

    for col in vars:
        if col == "a":
            add_a()
        if col == "b":
            add_b()
        if col == "c":
            add_c()
        if col == "d":
            add_d()
        if col == "e":
            add_e()
        if col == "f":
            add_f()
        if col == "g":
            add_g()

    print("Finding 1 solution...")
    sol1 = problem.getSolution()
    print(sol1)
    print("Finding 1 solution complete...")

    print("Finding all solutions...")
    start = dt.datetime.now()

    if iterative:
        solutions = []
        for solution in problem.getSolutionIter():
            print(solution)
            solutions.append(solution)
            with open(
                f"export/{start_time}-{corpora_str}-{''.join(vars)}.jsonlines", "a"
            ) as f:
                f.write(json.dumps(solution) + "\n")
    else:
        solutions = problem.getSolutions()
    end = dt.datetime.now()
    print(f"Time taken: {(end-start).total_seconds()} seconds")
    print(f"# solutions: {len(solutions)}")

    return solutions


def expand_solutions(
    solutions_: list[dict[str, str]], columns: list[str]
) -> tuple[dict[str, list[str]], list[str]]:
    words = {}
    cols_with_data = []
    for col in columns:
        try:
            words[col] = [
                "".join([solution[f"{col}{i}"] for i in range(1, 6)])
                for solution in solutions_
            ]
            cols_with_data.append(col)
            # print(f"{col}: {words[col]}")
        except KeyError:
            words[col] = [" " * 5] * len(solutions_)
            continue
    return words, cols_with_data


def expand_solution(
    solution_: dict[str, str], columns: list[str]
) -> tuple[dict[str, list[str]], list[str]]:
    words = {}
    cols_with_data = []
    for col in columns:
        try:
            words[col] = ["".join([solution_[f"{col}{i}"] for i in range(1, 6)])]
            cols_with_data.append(col)
            # print(f"{col}: {words[col]}")
        except KeyError:
            words[col] = [" " * 5]
            continue
    return words, cols_with_data


def replace(words: dict[str, list[str]], col: str, alt: str, col_i: int, alt_i: int):
    if col_i > 5 or alt_i > 5:
        raise ValueError("Index to High")
    return [
        col[:col_i] + alt[alt_i] + col[col_i + 1 :]
        for col, alt in zip(words[col], words[alt])
    ]


def add_missing_data(words_: dict[str, list[str]], columns, cols_with_data):
    """add in data for which we didn't fill using the solver"""
    for col in sorted(list(set(columns) - set(cols_with_data))):
        if col == "d":
            # replace d2 with c2
            words_[col] = replace(words_, col=col, alt="c", col_i=1, alt_i=1)
            # replace d4 with a3
            words_[col] = replace(words_, col=col, alt="a", col_i=3, alt_i=2)
            # replace d5 with a3
            words_[col] = replace(words_, col=col, alt="a", col_i=4, alt_i=2)
        elif col == "e":
            # replace e1 with a3
            words_[col] = replace(words_, col=col, alt="a", col_i=0, alt_i=2)
            # replace e3 with a1
            words_[col] = replace(words_, col=col, alt="a", col_i=2, alt_i=0)
            # replace e4 with a3
            words_[col] = replace(words_, col=col, alt="a", col_i=3, alt_i=2)
        elif col == "f":
            # replace f5 with a5
            words_[col] = replace(words_, col=col, alt="a", col_i=4, alt_i=4)
        elif col == "g":
            # replace g1 with a1
            words_[col] = replace(words_, col=col, alt="a", col_i=0, alt_i=0)
            # replace g2 with a3
            words_[col] = replace(words_, col=col, alt="a", col_i=1, alt_i=2)
            # replace g3 with c2
            words_[col] = replace(words_, col=col, alt="c", col_i=2, alt_i=1)
    return words_


def add_final_words(words_: dict[str, list[str]], columns) -> dict[str, list[str]]:
    """Create final words and add"""
    final_words = []
    for a, b, c, d, e, f in zip(*[words_[col] for col in columns[:-1]]):
        # print(a, b, c, d, e, f)
        final_words.append(a[0] + b[1] + c[1] + d[4] + e[1] + f[3])

    words_["final"] = final_words
    return words_


# Export to excel
def export(words, cols_with_data, corpora: list[str]):
    corpora_str = "_".join(corpora)
    cols_str = "".join(list(cols_with_data))
    now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    data = pd.DataFrame(data=words).T
    # Select max number of columns
    data = data.iloc[:, :16384]
    data.to_excel(f"export/{now}-{corpora_str}-{cols_str}.xlsx")


def main():
    iterative = True
    corpora = ["LINGO", "MWB", "WORDFEUD"]
    corpus = retrieve_corpus(datasets=corpora)
    print(f"Using Corpora: {corpora}")
    print(f"Corpus size: {len(corpus)}")
    columns = list("abcdefg")

    # Postprocess words into solution
    solutions = csp(corpus, corpora=corpora, vars=list("abcefg"), iterative=iterative)
    words, cols_with_data = expand_solutions(solutions, columns)

    words = add_missing_data(words, columns, cols_with_data)
    words = add_final_words(words, columns)
    export(words, cols_with_data, corpora)


if __name__ == "__main__":
    main()
