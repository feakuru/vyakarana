from itertools import product
from typing import Dict, List, Tuple, Union

from vyakarana.part_of_speech import PartOfSpeech
from vyakarana.vocabulary import Vocabulary


class GrammarFitter:
    """
    Given a vocabulary and a set of parts of speech,
    attempts to fit a given word to a valid combination
    of part of speech and permutation values.
    """

    def __init__(
        self,
        parts_of_speech: List[PartOfSpeech],
        vocabulary: Dict[str, List[str]],
    ):
        self.parts_of_speech = parts_of_speech
        self.vocabulary = Vocabulary(vocabulary)

    def fit(self, word: str) -> Union[
        str,
        List[Tuple[PartOfSpeech, Dict[str, str]]],
    ]:
        """
        Attempt to fit the given word to a valid combination
        of part of speech and permutation values.
        If a valid combination is found, returns a tuple
        of the part of speech and the permutation values.
        If no valid combination is found, returns the original word.
        """
        result = []
        for pos in self.parts_of_speech:
            for strategy in pos.permutation_strategies:
                for word_permutation in self._generate_permutations(
                    word,
                    strategy,
                ):
                    permutation_values = self._match_permutation(
                        pos,
                        word_permutation,
                    )
                    if permutation_values:
                        result.append((pos.name, permutation_values))
        return result

    def _generate_permutations(self, word: str, strategy: str) -> List[str]:
        """
        Generate permutations of the given word based on the given strategy.
        """
        if strategy == 'default':
            return [word]
        raise ValueError(f"Strategy {strategy} not implemented.")

    def _match_permutation(
        self,
        part_of_speech: PartOfSpeech,
        word_permutation: str,
    ) -> Union[None, List[Dict[str, str]]]:
        """
        Attempt to match the given word permutation to the given part
        of speech, returning the permutation values if a match is found
        or None otherwise.
        """
        permutation_values = []
        all_permutations = list(product(
            *part_of_speech.permutation_dimensions.values()
        ))
        for permutation in all_permutations:
            permutation = dict(zip(
                part_of_speech.permutation_dimensions.keys(),
                permutation,
            ))
            try:
                words = self.vocabulary.get_words(
                    part_of_speech=part_of_speech.name,
                )
                # print(f'trying {permutation=} with {words=}')
                for word in words:
                    permuted = part_of_speech.permute(
                        word=word,
                        **permutation,
                    )
                    # print(f'{permuted=}')
                    if word_permutation == permuted:
                        permutation_values.append(permutation)
            except ValueError:
                pass  # permutation not valid for these dimensions
        return permutation_values
