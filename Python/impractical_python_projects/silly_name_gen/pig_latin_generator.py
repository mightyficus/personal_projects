"""Generate a pig-latin translation from a given sentence"""

def main():
    """If the first letter of a string is a consonant, put it at the end and 
    add "ay". If it starts with a vowel, just add "way" to the end.
    """

    while True:
        start_sentence = input("Enter a sentence to translate: ")

        # Cleans up leading and trailing whitespace, then splits sentence
        # into individual words
        wordlist = start_sentence.strip().split()

        pig_latin = ""
        for word in wordlist:
            # If the word starts with a vowel, just add "way" to the end
            if word[0] in "aeiou":
                pig_latin = pig_latin + word + "way "
            # If the word startss in a composite sound, move the whole sound
            elif word[0:2].lower() in ['ch', 'sh', 'th', 'wh', 'ph']:
                pig_latin = pig_latin + word[2:] + word[0:2] + 'ay '
            else:
                pig_latin = pig_latin + word[1:] + word[0] + 'ay '

        print(f'\n\nYour sentence in Pig Latin is: {pig_latin}')

        try_again = input("\n\nTry again? (Press Enter else n to quit: ")
        if try_again.lower() == 'n':
            break

if __name__ == "__main__":
    main()
