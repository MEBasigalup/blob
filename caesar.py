# Import functions
from sys import argv
from cs50 import get_string

# Make sure user input is correct
if len(argv) != 2:
    exit("Usage: python caesar.py n")

if argv[1].isdigit == False:
    exit("Usage: python caesar.py n")

# Key
n = int(argv[1])
if n <= 0:
    exit("Usage: python caesar.py n")

plaintext = get_string("Plaintext: ")

# Print ciphertext
print("ciphertext: ", end="")

for c in plaintext:

    # Upper cap characters
    if c.islower() == True:
        # Convert to ascii
        a = ord(c) - 97
        # Use key
        a = (a+n) % 26
        # Convert back to characters
        aa = chr(a+97)
        print(aa, end="")

    # Lower cap characters
    elif c.isupper() == True:
        # Convert to ascii
        b = ord(c) - 65
        # Use key
        b = (b+n) % 26
        # Convert back to characters
        bb = chr(b+65)
        print(bb, end="")

    # Non-text characters
    else:
        print(c, end="")
print()