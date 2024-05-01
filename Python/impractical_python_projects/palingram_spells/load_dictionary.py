"""Load a text file as a list

Arguments:
-text file name (and directory path, if needed)

Exceptions:
-IOError if filename not found

Reurns:
-A list of all words in a text file in lower case

Requires-import sys
"""
import sys

def load(file):
    """Open a text file and return a list of lowercase strings."""
    try:
        with open(file) as ifile:
            loaded_txt = ifile.read().strip().split('\n')
            loaded_txt = [x.lower() for x in loaded_txt]
            return loaded_txt
    except IOError as e:
        print(f"{e}\nError opening {file}. Terminating program.",
              file=sys.stderr)
        sys.exit(1)
