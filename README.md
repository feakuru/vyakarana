# VYĀKARAṆA

**Vyākaraṇa** is a grammar engine that provides a capability for users to create *grammar fitters*: classifiers that, given a word in the language, can suggest all possible permutations of words from the vocabulary of that language that fit that word.

To create a `GrammarFitter`, define it with the parameters of your language:

Please write code for the vyakarana module that can be used like this:

```python
from vyakarana import PartOfSpeech, Vocabulary, GrammarFitter


def verb_permute(word, tense, person, number):
    if tense == 'past':
        return word + 'ed'
    elif tense == 'present':
        if number == 'singular' and person == '3':
            return word + 's'
        return word
    raise

verb = PartOfSpeech(
    permutation_dimensions={
        'tense': ['past', 'present'],
        'person': ['1', '2', '3',],
        'number': ['singular', 'plural'],
    },
    permutation_strategies=['1st conjugation'],
    permutation_function=verb_permute,
)

def noun_permute(word, case, number):
    if number == 'singular':
        if case == 'posessive':
            return word + '\'s'
        return word
    elif number == 'plural':
        if case == 'posessive':
            return word + 's\''
        return word + 's'
    raise

noun = PartOfSpeech(
    permutation_dimensions={
        'case': ['subjective', 'objective', 'posessive'],
        'number': ['singular', 'plural'],
    },
    permutation_strategies=['default'],
    permutation_function=noun_permute,
)

fitter = GrammarFitter(
    parts_of_speech=[verb, noun, article],
    vocabulary={
        'noun': ['bread', 'milk', 'toast'],
        'verb': ['cook', 'reveal', 'show']
    }
)

fitter.fit('milks\'')  # milk, noun, plural, posessive
fitter.fit('cooked')  # cool, verb, plural, past, [1, 2, 3] 
```