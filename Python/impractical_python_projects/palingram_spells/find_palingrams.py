"""Find all word-pair palingrams given a dictionary file"""
from load_dictionary import load

word_list = load("dict_2of4brif.txt")

# def find_palingrams():
#     palingram_list = []
#     for first_word in word_list:
#         for second_word in word_list:
#             possible = ''.join([first_word, second_word])
#             if possible == possible[::-1]:
#                 #print(' '.join([first_word, second_word]))
#                 palingram_list.append(' '.join([first_word, second_word]))
#     return palingram_list

# find word pair palingrams
def find_palingrams():
    """Find dictionary palingrams"""
    pali_list = []
    words = set(word_list)
    for word in words:
        # For each word, find its length
        # Word's length determines the indexes the program uses to slice 
        # through the word, looking for every possible reversed 
        # word-palindromic sequence combo
        end = len(word)
        # Reverse the word
        rev_word = word[::-1]
        # Exclude 1 letter words
        if end > 1:
            # Loop through letters in the current word
            for i in range (end):
                # Require the back end of the word to be palindromic and the
                # front end to be a reverse word in the word list
                if word[i:] == rev_word[:end-i] and rev_word[end-i:] in words:
                    pali_list.append((word, rev_word[end-i:]))
                # Repeat the conditional, but reverse the output
                if word[:i] == rev_word[end-i:] and rev_word[:end-i] in words:
                    pali_list.append((rev_word[:end-i], word))
    return pali_list

palingrams = find_palingrams()

# Sort palingrams based on first word
palingrams_sorted = sorted(palingrams)

# Display list of palingrams
print(f"\nNumber of palingrams = {len(palingrams_sorted)}\n")
for words in palingrams_sorted:
    print(f'{words[0]} {words[1]}')