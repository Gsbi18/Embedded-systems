def caesar(msg, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_message = ""
    msg=msg.lower()
    for i in msg:
        position = alphabet.find(i)
        new_position = (position + key) % len(alphabet)
        new_character = alphabet[new_position]
        new_message += new_character
    return new_message
key = 3
while True:
    message = input("Please enter a message: ")
    if message == "q": break
    encry_message = caesar(message, key)
    decry_message = caesar(encry_message, -key)
    print("Encrypted message: ", encry_message)
    print("Encrypted message: ", decry_message)
    