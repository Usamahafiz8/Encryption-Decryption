import re

def generate_key_square(key):
    # Remove non-alphabetic characters from the key
    key = re.sub('[^A-Za-z]', '', key).upper()
    # Create the key square with unique letters from the keyword
    key_square = "".join(sorted(set(key + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), key=key.index))
    return key_square

def playfair(plaintext, key, encrypt=True):
    key_square = generate_key_square(key)
    plaintext = re.sub('[^A-Za-z]', '', plaintext).upper()

    # Create a list of character pairs
    pairs = [(plaintext[i], plaintext[i+1]) if i+1 < len(plaintext) and plaintext[i] != plaintext[i+1] else (plaintext[i], 'X') for i in range(0, len(plaintext), 2)]

    # Encrypt or decrypt each pair of characters
    result = ""
    for char1, char2 in pairs:
        # Get the coordinates of each character in the key square
        idx1, idx2 = map(key_square.index, (char1, char2))
        row1, col1 = divmod(idx1, 5)
        row2, col2 = divmod(idx2, 5)

        # Encrypt or decrypt the characters in the same row
        if row1 == row2:
            result += key_square[row1*5 + (col1+1)%5] if encrypt else key_square[row1*5 + (col1-1)%5]
            result += key_square[row2*5 + (col2+1)%5] if encrypt else key_square[row2*5 + (col2-1)%5]
        # Encrypt or decrypt the characters in the same column
        elif col1 == col2:
            result += key_square[((row1+1)%5)*5 + col1] if encrypt else key_square[((row1-1)%5)*5 + col1]
            result += key_square[((row2+1)%5)*5 + col2] if encrypt else key_square[((row2-1)%5)*5 + col2]
        # Encrypt or decrypt the characters in different rows and columns
        else:
            result += key_square[row1*5 + col2]
            result += key_square[row2*5 + col1]

    # Remove any padding 'X' characters
    result = re.sub('X$', '', result)

    return result

# Prompt the user for input and encrypt the plaintext
plaintext = input("Enter plaintext: ")
key = input("Enter key: ")
ciphertext = playfair(plaintext, key)
print("Ciphertext:", ciphertext)

# Decrypt the ciphertext
ciphertext = input("Enter ciphertext: ")
key = input("Enter key: ")
plaintext = playfair(ciphertext, key, encrypt=False)
print("Plaintext:", plaintext)
