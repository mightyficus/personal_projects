"""Takes a string and and returns a simple bar chart of each letter"""

import pprint
from collections import defaultdict

text = 'Like the castle in its corner in a medieval game, I forsee a \
    terrible trouble, and I stay here just the same.'

mapped = defaultdict(list)
for char in text:
    if char.isalpha():
        mapped[char.lower()].append(char.lower())

pprint.pprint(mapped, width=110)
