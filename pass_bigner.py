import random
import string

print(" Random Password Generator")

try:
    length = int(input("Enter password length: "))

    if length <= 0:
        print("Length must be positive")
        exit()

    letters = input("Include letters? (y/n): ").lower() == 'y'
    numbers = input("Include numbers? (y/n): ").lower() == 'y'
    symbols = input("Include symbols? (y/n): ").lower() == 'y'

    characters = ""

    if letters:
        characters += string.ascii_letters
    if numbers:
        characters += string.digits
    if symbols:
        characters += string.punctuation

    if characters == "":
        print("Please select at least one character type.")
        exit()

    password = "".join(random.choice(characters) for i in range(length))

    print("\nGenerated Password:", password)

except ValueError:
    print("Invalid input. Enter numeric value.")
