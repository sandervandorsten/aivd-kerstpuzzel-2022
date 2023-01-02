from dataclasses import dataclass
from itertools import product
import datetime as dt
from pathlib import Path

from constraint import *

pieces = {
    "WK": 100,
    "WQ": 10,
    "WI": 6,  # Nightrider
    "WR": 5,
    "WB": 3.01,
    "WN": 3.02,
    "WG": 2,  # Grasshopper (inverted queen)
    "WP": 1,
    "BK": -100,
    "BQ": -10,
    "BI": -6,  # Nightrider
    "BR": -5,
    "BB": -3.01,
    "BN": -3.02,
    "BG": -2,  # Grasshopper (inverted queen)
    "BP": -1,
}
pieces_inv = {v: k for k, v in pieces.items()}
columns = list("abcdefgh")
rows = list(map(str, range(1, 9)))


class RoundedSumConstraint(ExactSumConstraint):
    """
    Constraint enforcing that values of given variables sum roughly
    to a given amount
    """

    def preProcess(self, variables, domains, constraints, vconstraints):
        Constraint.preProcess(self, variables, domains, constraints, vconstraints)
        multipliers = self._multipliers
        exactsum = self._exactsum
        if multipliers:
            raise NotImplementedError()
            # for variable, multiplier in zip(variables, multipliers):
            #     domain = domains[variable]
            #     for value in domain[:]:
            #         if round(value) * multiplier > exactsum:
            #             domain.remove(value)
        else:
            pass
            # Don't prune values
            # for variable in variables:
            #     domain = domains[variable]
            #     for value in domain[:]:
            #         if round(value) > exactsum:
            #             domain.remove(value)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        multipliers = self._multipliers
        exactsum = self._exactsum
        sum = 0
        missing = False
        if multipliers:
            raise NotImplementedError
            # for variable, multiplier in zip(variables, multipliers):
            #     if variable in assignments:
            #         sum += assignments[variable] * multiplier
            #     else:
            #         missing = True
            # if type(sum) is float:
            #     sum = round(sum)
            # if sum > exactsum:
            #     return False
            # if forwardcheck and missing:
            #     for variable, multiplier in zip(variables, multipliers):
            #         if variable not in assignments:
            #             domain = domains[variable]
            #             for value in domain[:]:
            #                 if sum + value * multiplier > exactsum:
            #                     domain.hideValue(value)
            #             if not domain:
            #                 return False
        else:
            # create sum based on variable assignments
            for variable in variables:
                if variable in assignments:
                    sum += assignments[variable]
                else:
                    missing = True
            sum = round(sum)
            # DONT EXCLUDE VALUES IF LARGER THAN exactsum because we are above and below 0
            # if sum > exactsum:
            #     return False
            # if forwardcheck and missing:
            #     for variable in variables:
            #         if variable not in assignments:
            #             domain = domains[variable]
            #             for value in domain[:]:
            #                 if sum + value > exactsum:
            #                     domain.hideValue(value)
            #             if not domain:
            #                 return False
        if missing:
            return True
        else:
            return sum == exactsum


@dataclass
class Cage:
    """Cage"""

    vars: list[str]
    sum: int


class Variable(object):
    """
    Helper class for variable definition

    Using this class is optional, since any hashable object,
    including plain strings and integers, may be used as variables.
    """

    def __init__(self, name: str, value: int):
        """
        @param name: Generic variable name for problem-specific purposes
        @type  name: string
        @param value: Value of the variable
        @type  value: integer
        """
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.value.__eq__(other.value)
        else:
            print(f"equality check for var {other} with type {type(other)}")
            return self.value.__eq__(other)

    def __hash__(self):
        return self.name.__hash__()

    def __neq__(self, other):
        if isinstance(other, Variable):
            return not self.value.__eq__(other.value)
        else:
            print(f"non-equality check for var {other} with type {type(other)}")
            return not self.value.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Variable):
            return Variable(name=self.name, value=self.value + other.value)
        else:
            print(f"addition for var {other} with type {type(other)}")
            return Variable(name=self.name, value=self.value + other)

    def __radd__(self, other):
        return other + self.value

    def __mul__(self, other):
        if isinstance(other, Variable):
            return Variable(name=self.name, value=self.value * other.value)
        else:
            print(f"multiplication for var {other} with type {type(other)}")
            return Variable(name=self.name, value=self.value * other)

    def __rmul__(self, other):
        return other.value.__mul__(self.value)

    def __floordiv__(self, other):
        return Variable(name=self.name, value=self.value.__floordiv__(other.value))

    def __sub__(self, other):
        if isinstance(other, Variable):
            return Variable(name=self.name, value=self.value - other.value)
        else:
            print(f"subtraction for var {other} with type {type(other)}")
            return Variable(name=self.name, value=self.value - other)

    def __rsub__(self, other):
        return other - self.value

    def __le__(self, other):
        if isinstance(other, Variable):
            return self.value <= other.value
        else:
            return self.value <= other

    def __lt__(self, other):
        if isinstance(other, Variable):
            return self.value < other.value
        else:
            return self.value < other

    def __gt__(self, other):
        if isinstance(other, Variable):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, Variable):
            return self.value >= other.value
        else:
            return self.value >= other


def main():
    start_time = dt.datetime.now()
    # pieces_vars = {
    #     "WK": Variable(name="WK", value=100),
    #     "WQ": Variable(name="WQ", value=10),
    #     "WI": Variable(name="WI", value=6),  # Nightrider
    #     "WR": Variable(name="WR", value=5),
    #     "WB": Variable(name="WB", value=3),
    #     "WN": Variable(name="WN", value=3),
    #     "WG": Variable(name="WG", value=2),  # Grasshopper (inverted queen)
    #     "WP": Variable(name="WP", value=1),
    #     "BK": Variable(name="BK", value=-100),
    #     "BQ": Variable(name="BQ", value=-10),
    #     "BI": Variable(name="BI", value=-6),  # Nightrider
    #     "BR": Variable(name="BR", value=-5),
    #     "BB": Variable(name="BB", value=-3),
    #     "BN": Variable(name="BN", value=-3),
    #     "BG": Variable(name="BG", value=-2),  # Grasshopper (inverted queen)
    #     "BP": Variable(name="BP", value=-1),
    # }
    solver = BacktrackingSolver()
    print(f"solver = {type(solver).__name__}")
    problem = Problem(solver=solver)
    # Create 8x8 variables

    variables = ["".join(x) for x in product(columns, rows)]

    # Variables
    # pin some variables to a specific domain
    problem.addVariable("e1", [pieces["WK"]])
    problem.addVariable("g1", [pieces["BK"]])
    problem.addVariable("e2", [pieces["WP"]])
    problem.addVariable("h2", [pieces["BP"]])
    problem.addVariable("f3", [pieces["WB"]])
    problem.addVariable("h1", [pieces["WN"]])  # White Knight moved from g3 to h1
    problem.addVariable("g5", [pieces["WP"]])
    problem.addVariable("f7", [pieces["BP"]])
    problem.addVariable("g7", [pieces["WR"]])
    # problem.addVariable("e1", [pieces_vars["WK"]])
    # problem.addVariable("g1", [pieces_vars["BK"]])
    # problem.addVariable("e2", [pieces_vars["WP"]])
    # problem.addVariable("h2", [pieces_vars["BP"]])
    # problem.addVariable("f3", [pieces_vars["WB"]])
    # problem.addVariable("h1", [pieces_vars["WN"]])  # White Knight moved from g3 to h1
    # problem.addVariable("g5", [pieces_vars["WP"]])
    # problem.addVariable("f7", [pieces_vars["BP"]])
    # problem.addVariable("g7", [pieces_vars["WR"]])

    # fill all variables with default domain
    undeclared_vars = [var for var in variables if var not in problem._variables]
    problem.addVariables(undeclared_vars, list(pieces.values()))

    # Constraints

    # All values in column need to be different
    for col in columns:
        vars_in_col = [var for var in variables if col in var]
        problem.addConstraint(AllDifferentConstraint(), vars_in_col)

    # All values in row need to be different
    for row in rows:
        vars_in_row = [var for var in variables if row in var]
        problem.addConstraint(AllDifferentConstraint(), vars_in_row)

    # All values in quadrants need to be different
    size = 4
    amount = 2
    for i in range(amount):
        for j in range(amount):
            quadrant_cols = columns[i * size : (i + 1) * size]
            quadrant_rows = rows[j * size : (j + 1) * size]
            vars_in_quadrant = [
                "".join(x) for x in product(quadrant_cols, quadrant_rows)
            ]
            problem.addConstraint(AllDifferentConstraint(), vars_in_quadrant)

    # define cages (from bottomleft to topright, just like the ordering is with chess
    # for maximum consistency
    cages = [
        Cage(vars=["a1", "b1"], sum=-8),
        Cage(vars=["c2", "c1"], sum=11),
        Cage(vars=["d2", "d1"], sum=-5),
        Cage(vars=["e2", "e1", "f1", "g1", "h1", "f2", "g2", "h2"], sum=-4),
        Cage(vars=["a3", "a2"], sum=9),
        Cage(vars=["b3", "b2"], sum=0),
        Cage(vars=["c3", "c4"], sum=0),
        Cage(vars=["e3", "f3", "g3", "h3"], sum=-14),
        # Cage(vars=["b4", "c4"], sum=0),  # Difficult
        Cage(vars=["e4", "f4", "f5"], sum=13),
        Cage(vars=["a5", "a4", "b5"], sum=-5),
        Cage(vars=["g5", "g4", "h4", "h5"], sum=18),
        Cage(vars=["a6", "b6"], sum=-1),
        Cage(vars=["c6", "c5"], sum=-4),
        # Cage(vars=["d6", "d5", "d4", "e6", "e5"], sum=-102),  # Difficult
        Cage(vars=["b7", "c7", "d7"], sum=14),
        Cage(vars=["e7", "f7", "f6"], sum=-1),
        Cage(vars=["a8", "b8", "a7"], sum=92),
        Cage(vars=["c8", "d8", "e8", "f8"], sum=0),  # Difficult
        Cage(vars=["g8", "h8", "g7", "h7"], sum=0),
    ]
    print(f"#n cages: {len(cages)}")
    for cage in cages:
        problem.addConstraint(AllDifferentConstraint(), cage.vars)
        problem.addConstraint(RoundedSumConstraint(cage.sum), cage.vars)

    if isinstance(solver, BacktrackingSolver):
        for i, solution in enumerate(problem.getSolutionIter()):
            if i > 10000:
                break
            export(solution, i, start_time, len(cages))
    else:
        solution = problem.getSolution()
        export(solution, 0, start_time, len(cages))


def export(
    solution: list[dict[str, int]], i: int, start_time: dt.datetime, n_cages: int
):
    now = start_time.strftime("%Y%m%d-%H%M%S")
    folder = Path(f"export/{n_cages}/{now}")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / Path(f"{i}.sudoku")

    string = ""
    for row in reversed(rows):
        for col in columns:
            string += pieces_inv[solution[f"{col}{row}"]] + "\t"
        string += "\n"
    print(string)
    with open(path, "w") as f:
        f.write(string)


if __name__ == "__main__":
    main()
