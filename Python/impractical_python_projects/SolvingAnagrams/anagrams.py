"""Find anagrams in a single word"""
import load_dictionary

word_list = load_dictionary.load('dict_2of4brif.txt')

anagram_list = []

# Input a single word or single name below to find its anagram
name = 'henial'
print(f'Input Name: {name}')

name = name.lower()
print(f'Using name {name}')

# Sort name and find anagrams
name_sorted = sorted(name)
for word in word_list:
    word = word.lower()
    if word != name:
        if sorted(word) == name_sorted:
            anagram_list.append(word)

# Print out list of anagrams
print()
if len(anagram_list) == 0:
    print("No anagrams found! Change the name or find a bigger dictionary!")
else:
    print('Anagrams:', *anagram_list, sep='\n')