import itertools
import string
from typing import Literal
import pandas as pd

from data.wordfeud import wordfeud_corpus
from data.lingo import lingo_corpus

dataset = Literal["LINGO", "MWB", "WORDFEUD"]


def check_word(word: str) -> bool:
    return len(word) == 5 and word.isascii()


def preproces_word(word: str) -> str:
    return word.lower()


def preprocess_lingo() -> list[str]:
    return [preproces_word(word) for word in lingo_corpus if check_word(word)]


def preprocess_wordfeud() -> list[str]:
    return [preproces_word(word) for word in wordfeud_corpus if check_word(word)]


def preprocess_mijnwoordenboek() -> list[str]:
    mwb = pd.read_csv("data/corpus-mijnwoordenboek.csv", names=["word"], dtype="string")
    # keep only ASCII words
    mwb = mwb[mwb["word"].map(str.isascii)]
    # make lowercase
    mwb["word"] = mwb["word"].str.lower()
    return mwb["word"].to_list()


def retrieve_corpus(datasets: list[str] = ("LINGO", "MWB", "WORDFEUD")):
    nested_corpus = []
    if "LINGO" in datasets:
        nested_corpus.append(preprocess_lingo())
    if "WORDFEUD" in datasets:
        nested_corpus.append(preprocess_wordfeud())
    if "MWB" in datasets:
        nested_corpus.append(preprocess_mijnwoordenboek())
    corpus = list(set(itertools.chain(*nested_corpus)))
    return corpus
