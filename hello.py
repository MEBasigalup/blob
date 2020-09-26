# Import function to retrieve string from user
from cs50 import get_string

# Ask user their name
s = get_string("What is your name?")

# Salute user
print("hello, ", s)