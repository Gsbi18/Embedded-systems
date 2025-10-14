from random import randint

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
def generate_otp(characters):
    with open("otp.txt", "w") as f:
        for i in range(characters):
            f.write(str(randint(0,26)) + "\n")
            

def load_otp():
    with open("otp.txt", "r") as f:
        contents = f.read().splitlines()
    return contents


def encrypt(message, key):
    ciphertext = ''
    for (position, character) in enumerate(message):
        if character not in ALPHABET:
            ciphertext += character
        else:
            encrypted = (ALPHABET.index(character) + int(key[position])) % len(ALPHABET)
            ciphertext += ALPHABET[encrypted]
            return ciphertext
        
        
def decrypt(message, key):
    ciphertext = ''
    for (position, character) in enumerate(message):
        if character not in ALPHABET:
            ciphertext += character
        else:
            encrypted = (ALPHABET.index(character) + int(-key[position])) % len(ALPHABET)
            ciphertext += ALPHABET[encrypted]
            return ciphertext
        
key = 3
while True:
    message = input("Please enter a message: ")
    if message == "q": break
    encry_message = encrypt(message, key)
    decry_message = decrypt(encry_message, -key)
    print("Encrypted message: ", encry_message)
    print("Encrypted message: ", decry_message)