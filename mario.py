# Import funciont to ask for integer
from cs50 import get_int

# Prompt user for pyrammid height
while True:
    h = get_int("Height: ")

    # Check pyramid height is between 1 and 8
    if h < 9 and h > 0:
        break

# Loop for pyramid height
for i in range(h):
    # Printing spaces in each row
    for k in range(h-i-1):
        print(" ", end="")
    # Printing hashes in each row
    for j in range(i+1):
        print("#", end="")
    print()