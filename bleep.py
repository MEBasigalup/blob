from cs50 import get_string
from sys import argv


def main():

    if len(argv) != 2:
        exit("Usage: python bleep.py dictionary.txt")

    # Define empty set
    words = set()

    # Define dictionary
    dictionary = open(argv[1])

    # Load dictionary
    for line in dictionary:
        words.add(line.strip().lower())

    # Input text
    input = get_string("What message would you like to censor?\n").split()
    # Output text
    bleep = ""

    # Cheack if it is a bad word on the dictionary
    for word in input:
        # If so, replace with hashes
        if word.lower() in words:
            bleep += "*" * len(word) + " "
        # If not, leave unchanged
        else:
            bleep += word + " "

    # Return censored message
    print(bleep.strip())


if __name__ == "__main__":
    main()