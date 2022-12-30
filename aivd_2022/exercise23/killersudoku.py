from dataclasses import dataclass
from itertools import product

from constraint import Problem, AllDifferentConstraint, ExactSumConstraint


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
            print(f"equality check for var {other} with type {type(other}}")
            return self.value.__eq__(other)
    def __neq__(self, other):
        if isinstance(other, Variable):
            return not self.value.__eq__(other.value)
        else:
            print(f"non-equality check for var {other} with type {type(other}}")
            return not self.value.__eq__(other)

    def __add__(self, other):
        return Variable(name=self.name, value=self.value.__add__(other.value))

    def __radd__(self, other):
        return other.value.__add__(self.value)

    def __mul__(self, other):
        return Variable(name=self.name, value=self.value.__mul__(other.value))

    def __rmul__(self, other):
        return other.value.__mul__(self.value)

    def __floordiv__(self, other):
        return Variable(name=self.name, value=self.value.__floordiv__(other.value))

    def __sub__(self, other):
        return Variable(name=self.name, value=self.value.__sub__(other.value))

    def __rsub__(self, other):
        return other.__sub__(self.value)

    def __le__(self, other):
        return self.value.__le__(other.value)

    def __lt__(self, other):
        return self.value.__lt__(other.value)

    def __gt__(self, other):
        return self.value.__gt__(other.value)

    def __ge__(self, other):
        return self.value.__ge__(other.value)


def main():
    pieces = {
        "WK": 100,
        "WQ": 10,
        "WI": 6,  # Nightrider
        "WR": 5,
        "WB": 3,
        "WN": 3,
        "WG": 2,  # Grasshopper (inverted queen)
        "WP": 1,
        "BK": -100,
        "BQ": -10,
        "BI": -6,  # Nightrider
        "BR": -5,
        "BB": -3,
        "BN": -3,
        "BG": -2,  # Grasshopper (inverted queen)
        "BP": -1,
    }

    pieces_vars = {
        Variable(name="WK", value= 100),
        Variable(name="WQ", value= 10),
        Variable(name="WI", value= 6),  # Nightrider
        Variable(name="WR", value= 5),
        Variable(name="WB", value= 3),
        Variable(name="WN", value= 3),
        Variable(name="WG", value= 2),  # Grasshopper (inverted queen)
        Variable(name="WP", value= 1),
        Variable(name="BK", value= -100),
        Variable(name="BQ", value= -10),
        Variable(name="BI", value= -6),  # Nightrider
        Variable(name="BR", value= -5),
        Variable(name="BB", value= -3),
        Variable(name="BN", value= -3),
        Variable(name="BG", value= -2),  # Grasshopper (inverted queen)
        Variable(name="BP", value= -1),
    }

    problem = Problem()
    # Create 8x8 variables
    columns = list("abcdefgh")
    rows = list(map(str, range(1, 9)))
    variables = ["".join(x) for x in product(columns, rows)]

    # Variables
    # pin some variables to a specific domain
    # problem.addVariable("e1", [pieces["WK"]])
    # problem.addVariable("g1", [pieces["BK"]])
    # problem.addVariable("e2", [pieces["WP"]])
    # problem.addVariable("h2", [pieces["BP"]])
    # problem.addVariable("f3", [pieces["WB"]])
    # problem.addVariable("h1", [pieces["WN"]])  # White Knight moved from g3 to h1
    # problem.addVariable("g5", [pieces["WP"]])
    # problem.addVariable("f7", [pieces["BP"]])
    # problem.addVariable("g7", [pieces["WR"]])
    # problem.addVariable("e1", [pieces["WK"]])
    # problem.addVariable("g1", [pieces["BK"]])
    # problem.addVariable("e2", [pieces["WP"]])
    # problem.addVariable("h2", [pieces["BP"]])
    # problem.addVariable("f3", [pieces["WB"]])
    # problem.addVariable("h1", [pieces["WN"]])  # White Knight moved from g3 to h1
    # problem.addVariable("g5", [pieces["WP"]])
    # problem.addVariable("f7", [pieces["BP"]])
    # problem.addVariable("g7", [pieces["WR"]])

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
        # cages = [
        #     Cage(vars=["a1", "b1"], sum=-8),
        # ]
        # for cage in cages:
        #     # problem.addConstraint(AllDifferentConstraint(), cage.vars)
        #     problem.addConstraint(ExactSumConstraint(cage.sum), cage.vars)

    sol = problem.getSolution()
    print(sol)
    x = 1


if __name__ == "__main__":
    main()
