
from typing import Dict, List


class PartOfSpeech:
    """
    Represents a part of speech and its possible permutations.
    """

    def __init__(
        self,
        name: str,
        permutation_dimensions: Dict[str, List[str]],
        permutation_strategies: List[str],
        permutation_function,
    ):
        self.name = name
        self.permutation_dimensions = permutation_dimensions
        self.permutation_strategies = permutation_strategies
        self.permutation_function = permutation_function

    def permute(
        self,
        word: str,
        **permutation_values,
    ) -> str:
        """
        Generate a permutation of this part of speech
        based on the given values.
        """
        for dimension in permutation_values.keys():
            if dimension not in self.permutation_dimensions:
                raise ValueError(
                    f'Dimension {dimension} not defined '
                    'for this part of speech.'
                )

        return self.permutation_function(word=word, **permutation_values)
