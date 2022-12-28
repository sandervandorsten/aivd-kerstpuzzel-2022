from collections import Counter
from pprint import pprint

import copy

text = "UV DCVOP BEG’P OE FE VLSEOPEFEPCJWP UQB WGE CH GP HCVFGQD OHMGBTE?"
cypher = {
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'i',
    'H': 'n',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 's',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'n',
    'V': 'a',
    'W': 'k',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',
}

solution = copy.copy(text)
for k, v in cypher.items():
    solution = solution.replace(k, v)


print(text)
print(solution)
# pprint(Counter(text))


