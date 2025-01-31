"""Find palindromes in a given dictionary file"""
from load_dictionary import load

word_list = load("2of4brif.txt")
pali_list = []

for word in word_list:
    if len(word) > 1 and word == word[::-1]:
        pali_list.append(word)

print(f'Number of palindromes found: {len(pali_list)}')
print(*pali_list, sep='\n')