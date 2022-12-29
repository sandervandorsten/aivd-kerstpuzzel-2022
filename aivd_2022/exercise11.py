from constraint import *
from collections import OrderedDict
import string

corpus = [
    "Acryl",
    "Affix",
    "Aftyp",
    "Ampex",
    "Accus",
    "Axels",
    "Acces",
    "Addax",
    "Afbik",
    "Afduw",
    "Afhap",
    "Afpik",
    "Afwis",
    "Afzag",
    "Afzak",
    "Afzeg",
    "Bobby",
    "Buggy",
    "Babys",
    "Baggy",
    "Buddy",
    "Buxus",
    "Bitch",
    "Blijf",
    "Bodys",
    "Bogey",
    "Bytes",
    "Batch",
    "Cycli",
    "Campy",
    "Crazy",
    "Crypt",
    "Chick",
    "Citys",
    "Curry",
    "Check",
    "Chijl",
    "Chimp",
    "Click",
    "Cocci",
    "Cyste",
    "Chips",
    "Cinch",
    "Codex",
    "Dizzy",
    "Dolby",
    "Dummy",
    "Derby",
    "Dolly",
    "Dixit",
    "Dicht",
    "Ducht",
    "Dacht",
    "Dandy",
    "Derny",
    "Detox",
    "Docht",
    "Douch",
    "Drijf",
    "Dwaze",
    "Epoxy",
    "Enzym",
    "Ethyl",
    "Exact",
    "Exces",
    "Echec",
    "Exlid",
    "Expat",
    "Expos",
    "Echel",
    "Essay",
    "Exman",
    "Extra",
    "Echos",
    "Echte",
    "Edoch",
    "Bobby",
    "Buggy",
    "Babys",
    "Baggy",
    "Buddy",
    "Buxus",
    "Bitch",
    "Blijf",
    "Bodys",
    "Bogey",
    "Bytes",
    "Batch",
    "Guppy",
    "Gipsy",
    "Gymde",
    "Gyros",
    "Gijpt",
    "Glimp",
    "Grijp",
    "Gejij",
    "Geluw",
    "Gepuf",
    "Glijd",
    "Glipt",
    "Gluip",
    "Gruwt",
    "Gulpt",
    "Gabbe",
    "Happy",
    "Hobby",
    "Husky",
    "Hyper",
    "Hypes",
    "Hypet",
    "Hypos",
    "Hysop",
    "Hapax",
    "Heavy",
    "Helix",
    "Hypen",
    "Hyven",
    "Hydra",
    "Hymen",
    "Hymne",
    "Intyp",
    "Ijzig",
    "Inbox",
    "Ijzel",
    "Ijsco",
    "Ijzer",
    "Index",
    "Icing",
    "Ijlst",
    "Ijsje",
    "Ijver",
    "Ijzen",
    "Ijdel",
    "Ijker",
    "Ijkte",
    "Ijlde",
    "Jazzy",
    "Jurys",
    "Jicht",
    "Juich",
    "Jacht",
    "Jacks",
    "Jozef",
    "Jawel",
    "Jouwt",
    "Jubel",
    "Jumbo",
    "Jajem",
    "Jalap",
    "Jambe",
    "Javel",
    "Jemig",
    "Kinky",
    "Kwijl",
    "Kruch",
    "Kucht",
    "Kwijt",
    "Kwips",
    "Kicks",
    "Kickt",
    "Kijft",
    "Kocht",
    "Krach",
    "Kuche",
    "Kwelm",
    "Kwijn",
    "Kicke",
    "Kijkt",
    "Lynch",
    "Lobby",
    "Lycra",
    "Lymfe",
    "Lolly",
    "Lycea",
    "Laque",
    "Lysol",
    "Ladys",
    "Licht",
    "Lucht",
    "Luxer",
    "Luxes",
    "Lacht",
    "Latex",
    "Lijft",
    "Mythe",
    "Mixed",
    "Mixer",
    "Mixes",
    "Mixte",
    "Macht",
    "Match",
    "Mezzo",
    "Mixen",
    "Mocht",
    "Macho",
    "Meluw",
    "Mikwa",
    "Mikwe",
    "Muffe",
    "Murwt",
    "Nimby",
    "Nicht",
    "Nylon",
    "Nacht",
    "Niche",
    "Nijpt",
    "Nixen",
    "Nabij",
    "Nanny",
    "Nihil",
    "Nijgt",
    "Nipje",
    "Nufje",
    "Nabob",
    "Naijl",
    "Napje",
    "Opzij",
    "Omwip",
    "Ofwel",
    "Olijf",
    "Opduw",
    "Opheb",
    "Ophef",
    "Oppik",
    "Opvul",
    "Opwek",
    "Opwel",
    "Opzag",
    "Opzak",
    "Opzeg",
    "Opzit",
    "Oxers",
    "Proxy",
    "Puppy",
    "Pique",
    "Pixel",
    "Paddy",
    "Party",
    "Pitch",
    "Pizza",
    "Pylon",
    "Pacht",
    "Panty",
    "Patch",
    "Pijpt",
    "Pocht",
    "Ponys",
    "Prach",
    "Query",
    "Quilt",
    "Quark",
    "Quads",
    "Quasi",
    "Quant",
    "Queue",
    "Quota",
    "Quote",
    "Rugby",
    "Rally",
    "Remix",
    "Riyal",
    "Radix",
    "Relax",
    "Richt",
    "Rouxs",
    "Ready",
    "Recht",
    "Rijft",
    "Rijpt",
    "Ruche",
    "Rabbi",
    "Ranch",
    "Rayon",
    "Squaw",
    "Schuw",
    "Sulky",
    "Sylfe",
    "Schip",
    "Schub",
    "Sfinx",
    "Shoyu",
    "Spray",
    "Syrah",
    "Schab",
    "Schaf",
    "Schap",
    "Schep",
    "Schik",
    "Schil",
    "Thyrs",
    "Tipsy",
    "Tyfus",
    "Tommy",
    "Types",
    "Typte",
    "Toque",
    "Twijg",
    "Typen",
    "Taxis",
    "Taxol",
    "Taxus",
    "Teddy",
    "Telex",
    "Tjilp",
    "Toddy",
    "Uzelf",
    "Unzip",
    "Upper",
    "Uglis",
    "Uilig",
    "Uitje",
    "Uiver",
    "Unica",
    "Uwent",
    "Uiige",
    "Uitga",
    "Ukken",
    "Ultra",
    "Unief",
    "Ureum",
    "Urmde",
    "Vinyl",
    "Vieux",
    "Vacht",
    "Vecht",
    "Vlijm",
    "Vocht",
    "Vijlt",
    "Vipje",
    "Vlijt",
    "Vlouw",
    "Vamps",
    "Vazal",
    "Vezel",
    "Views",
    "Vijst",
    "Vleze",
    "Wicht",
    "Wacht",
    "Wijze",
    "Winch",
    "Wrijf",
    "Wazig",
    "Weckt",
    "Wijkt",
    "Wijlt",
    "Wippe",
    "Wulps",
    "Webbe",
    "Welft",
    "Wezel",
    "Whist",
    "Wigje",
    "Xerox",
    "Xeres",
    "Xenon",
    "Yucca",
    "Yells",
    "Yogis",
    "Yanks",
    "Yards",
    "Yelde",
    "Yuans",
    "Zloty",
    "Zwijg",
    "Zwijm",
    "Zicht",
    "Zucht",
    "Zwalp",
    "Zwamp",
    "Zwilk",
    "Zacht",
    "Zocht",
    "Zwalk",
    "Zwelg",
    "Zwerf",
    "Zwiep",
    "Zwijn",
    "Zwikt",
]
corpus_lower = [word.lower() for word in corpus]
letters_unique_indices = [
    i for i, word in enumerate(corpus_lower) if len(set(word)) == len(word)
]
unique_words = [corpus_lower[letter] for letter in letters_unique_indices]

z = list(set([word[0] for word in unique_words]))
w = list(set([word[1] for word in unique_words]))
k = list(set([word[2] for word in unique_words]))
y = list(set([word[3] for word in unique_words]))
x = list(set([word[4] for word in unique_words]))
alphabet = list(string.ascii_lowercase)


def word_unique(x1, x2, x3, x4, x5):
    return x1 + x2 + x3 + x4 + x5 in unique_words


def in_corpus(x1, x2, x3, x4, x5):
    return x1 + x2 + x3 + x4 + x5 in corpus_lower


problem = Problem()

problem.addVariable("a1", z)
problem.addVariable("a2", w)
problem.addVariable("a3", k)
problem.addVariable("a4", y)
problem.addVariable("a5", x)

problem.addConstraint(
    lambda x1, x2, x3, x4, x5: word_unique(x1, x2, x3, x4, x5),
    ("a1", "a2", "a3", "a4", "a5"),
)

# B
problem.addVariable("b1", k)
problem.addVariable("b2", alphabet)
problem.addVariable("b3", alphabet)
problem.addVariable("b4", y)
problem.addVariable("b5", x)

problem.addConstraint(
    lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
    ("b1", "b2", "b3", "b4", "b5"),
)
problem.addConstraint(
    lambda x1, x2, x3, x4, x5, var: (
        (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
    ),
    ("b1", "b2", "b3", "b4", "b5", "a2"),
)
problem.addConstraint(
    lambda x1, x2, x3, x4, x5, var: (
        (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
    ),
    ("b1", "b2", "b3", "b4", "b5", "a1"),
)

# # C
problem.addVariable("c1", x)
problem.addVariable("c2", alphabet)
problem.addVariable("c3", k)
problem.addVariable("c4", alphabet)
problem.addVariable("c5", k)

problem.addConstraint(
    lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
    ("c1", "c2", "c3", "c4", "c5"),
)

problem.addConstraint(
    lambda x1, x2, x3, x4, x5, var: (
        (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
    ),
    ("c1", "c2", "c3", "c4", "c5", "a4"),
)

# TODO Deze constraint vind ie heel moeilijk, nakijken
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5, var: (
#         (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
#     ),
#     ("c1", "c2", "c3", "c4", "c5", "a1"),
# )

# TODO Deze constraint vind ie heel moeilijk, nakijken
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5, var: (
#         (x1 != var) & (x2 != var) & (x3 != var) & (x4 != var) & (x5 != var)
#     ),
#     ("c1", "c2", "c3", "c4", "c5", "b2"),
# )

# # D
# problem.addVariable("d1", x)
# problem.addVariable("d2", alphabet)
# problem.addVariable("d3", k)
# problem.addVariable("d4", alphabet)
# problem.addVariable("d5", k)
#
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
#     ("d1", "d2", "d3", "d4", "d5"),
# )
#
# # E
# problem.addVariable("e1", x)
# problem.addVariable("e2", alphabet)
# problem.addVariable("e3", k)
# problem.addVariable("e4", alphabet)
# problem.addVariable("e5", k)
#
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
#     ("e1", "e2", "e3", "e4", "e5"),
# )


# F
# problem.addVariable("f1", x)
# problem.addVariable("f2", alphabet)
# problem.addVariable("f3", k)
# problem.addVariable("f4", alphabet)
# problem.addVariable("f5", k)
#
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
#     ("f1", "f2", "f3", "f4", "f5"),
# )


# G
# problem.addVariable("g1", x)
# problem.addVariable("g2", alphabet)
# problem.addVariable("g3", k)
# problem.addVariable("g4", alphabet)
# problem.addVariable("g5", k)
#
# problem.addConstraint(
#     lambda x1, x2, x3, x4, x5: in_corpus(x1, x2, x3, x4, x5),
#     ("g1", "g2", "g3", "g4", "g5"),
# )

#### EQUAL CONSTRAINTS

# K
problem.addConstraint(
    lambda x1, x2: x1 == x2,
    ("a3", "b1"),
)

# TODO moelijk, nakijken.
# problem.addConstraint(
#     lambda x1, x2, x3: x1 == x2 == x3,
#     ("a3", "c3", "c5"),
# )

# X
problem.addConstraint(
    lambda x1, x2: x1 == x2,
    ("a5", "b5"),
)
problem.addConstraint(
    lambda x1, x2: x1 == x2,
    ("a5", "c3"),
)

# Y
problem.addConstraint(
    lambda x1, x2: x1 == x2,
    ("a4", "b4"),
)

print("starting solving...")
sol1 = problem.getSolution()
print(sol1)

solutions = problem.getSolutions()
words_found = [
    solution["a1"] + solution["a2"] + solution["a3"] + solution["a4"] + solution["a5"]
    for solution in solutions
]
words_found_b = [
    solution["b1"] + solution["b2"] + solution["b3"] + solution["b4"] + solution["b5"]
    for solution in solutions
]
words_found_c = [
    solution["c1"] + solution["c2"] + solution["c3"] + solution["c4"] + solution["c5"]
    for solution in solutions
]
print(words_found)
print(words_found_b)
print(words_found_c)
