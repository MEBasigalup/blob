# Import functions needed
from cs50 import get_float

# Prompt user for change
while True:
    change = get_float("Change owed: ")
    if change >= 0:
        break

# Counter
coins = 0

cash = round(change*100)

# >=25
if cash >= 25:
    coins += cash//25
    a = cash % 25

    if a >= 10:
        coins += a//10
        b = a % 10

        if b >= 5:
            coins += b//5
            c = b % 5

            coins += c//1
        else:
            coins += b//1

    elif a >= 5:
        coins += a//5
        b = a % 5

        coins += b//1

    else:
        coins += a//1

# >=10
elif cash >= 10:
    coins += cash//10
    d = cash % 10

    if d >= 5:
        coins += d//5
        e = d % 5

        if e >= 1:
            coins += e//1
    else:
        coins += d//1

# >=5
elif cash >= 5:
    coins += cash//5
    f = cash % 5
    coins += f//1

else:
    coins += cash//1

# Print number of coins
print(coins)