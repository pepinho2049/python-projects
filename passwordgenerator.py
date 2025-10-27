import string as s
import random

def generate_password(min_length, numbers = True, special_characters = True):
    letters = s.ascii_letters # creates a list with all the letters
    digits = s.digits # creates a list with all the digits
    special = s.punctuation # a list will all the special characters
    
    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special
    
    password = ''
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(password) < min_length:
        new_char = random.choice(characters)
        password += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True

        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special
    return password

pwd = generate_password(10)
print(pwd)