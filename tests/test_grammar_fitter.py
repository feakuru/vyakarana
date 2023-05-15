import pytest
from vyakarana.grammar_fitter import GrammarFitter
from vyakarana.part_of_speech import PartOfSpeech


def noun_permutator(word, case, number):
    if number == "singular":
        if case == "posessive":
            return word + "'s"
        return word
    elif number == "plural":
        if case == "posessive":
            return word + "s'"
        return word + "s"
    raise


def verb_permutator(word, tense, person, number):
    if tense == "past":
        return word + "ed"
    elif tense == "present":
        if number == "singular" and person == "3":
            return word + "s"
        return word
    raise


@pytest.mark.parametrize(
    ["word", "expected_fit_result"],
    [
        (
            "milks'",
            [("noun", [{"case": "posessive", "number": "plural"}])],
        ),
        (
            "cooked",
            [
                (
                    "verb",
                    [
                        {"number": "singular", "person": "1", "tense": "past"},
                        {"number": "plural", "person": "1", "tense": "past"},
                        {"number": "singular", "person": "2", "tense": "past"},
                        {"number": "plural", "person": "2", "tense": "past"},
                        {"number": "singular", "person": "3", "tense": "past"},
                        {"number": "plural", "person": "3", "tense": "past"},
                    ],
                )
            ],
        ),
        ("abba", []),
        (
            "cooks",
            [
                (
                    "verb",
                    [{
                        "number": "singular",
                        "person": "3",
                        "tense": "present",
                    }]
                ),
                (
                    "noun",
                    [
                        {"case": "subjective", "number": "plural"},
                        {"case": "objective", "number": "plural"},
                    ],
                ),
            ],
        ),
        ("cook's", [("noun", [{"case": "posessive", "number": "singular"}])]),
    ],
)
def test_grammar_fitter_simple_english(word, expected_fit_result):
    verb = PartOfSpeech(
        name="verb",
        permutation_dimensions={
            "tense": ["past", "present"],
            "person": ["1", "2", "3"],
            "number": ["singular", "plural"],
        },
        permutation_strategies=["default"],
        permutation_function=verb_permutator,
    )

    noun = PartOfSpeech(
        name="noun",
        permutation_dimensions={
            "case": ["subjective", "objective", "posessive"],
            "number": ["singular", "plural"],
        },
        permutation_strategies=["default"],
        permutation_function=noun_permutator,
    )

    fitter = GrammarFitter(
        parts_of_speech=[verb, noun],
        vocabulary={
            "noun": ["bread", "milk", "toast", "cook"],
            "verb": ["cook", "reveal", "show"],
        },
    )

    fit_result = fitter.fit(word)
    assert fit_result == expected_fit_result
