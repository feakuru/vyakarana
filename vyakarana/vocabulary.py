from typing import Dict, List


class Vocabulary:
    """
    A collection of words for each part of speech.
    """

    def __init__(self, words: Dict[str, List[str]]):
        self.words = words

    def get_words(self, part_of_speech: str) -> List[str]:
        # print(f'getting all {part_of_speech}s')
        return self.words.get(part_of_speech, [])
