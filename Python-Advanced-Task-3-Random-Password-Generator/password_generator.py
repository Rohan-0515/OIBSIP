import string
import random

try:
    length = int(input("Enter your password length: "))
except ValueError:
    print("Please enter a valid number.")
    exit()

characters = string.ascii_letters + string.digits + string.punctuation

if length < 4:
    print("Password length should be at least 4.")
else:
    lowercase = random.choice(string.ascii_lowercase)

    uppercase = random.choice(string.ascii_uppercase)

    number = random.choice(string.digits)

    special = random.choice(string.punctuation)

    required_characters = lowercase + uppercase + number + special

    remaining_length = length - 4

    remaining_characters = "".join(
        random.choice(characters) for _ in range(remaining_length)
    )

    password = required_characters + remaining_characters

    password_list = list(password)

    random.shuffle(password_list)

    password = " ".join(password_list)

    print("Generated Password:", password)
