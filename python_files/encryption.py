# Caesar Cipher Encryption

# Notes for myself
# 1) ord() convert char to ASCII position value
# 2) chr() convert ASCII position back to char
# ===============================================
# 3) Substract -65 for uppercased chars
# to become lowercased and back later
# ===============================================
# 4) Taking modulo % 26 to check if the values won't be
# bigger than 26 (our values must all be within 0 to 25)

# Initializing random shift size for caesar cypher
#s = np.random.randint(8)
s = 5

def encryption1_caesar(password, step=s):
    new_password = ""
    for char in str(password):
        # Handle if symbol is uppercased
        if char.isupper():
            new_password += chr((ord(char) + step - 65) % 26 + 65)
            continue
        # ... if symbol is lowercased
        if char.islower():
            new_password += chr((ord(char) + step - 97) % 26 + 97)
            continue
        if char.isdigit():
            new_password += str((int(char) + step) % 10)
        # ... if symbol is special symbol, leave them
        else:
            new_password += char
    return new_password


def encryption2_vigenere(password_caesar, key="TENIOVWNBSOOW"):
    new_pass = ""
    m = len(key)
    password_caesar = str(password_caesar)
    for char in range(len(password_caesar)):
        k = key[char % m]
        if password_caesar[char].isupper():
            new_pass += chr((ord(password_caesar[char]) - 65 + ord(k)) % 26 + 65)
            continue
        if password_caesar[char].islower():
            new_pass += chr((ord(password_caesar[char]) - 97 + ord(k)) % 26 + 97)
            continue
        if password_caesar[char].isdigit():
            new_pass += str((int(password_caesar[char]) + ord(k)) % 10)
        else:
            new_pass += password_caesar[char]
    return new_pass


def decryption1_vigenere(password_caesar, key="TENIOVWNBSOOW"):
    new_pass = ""
    m = len(key)
    password_caesar = str(password_caesar)
    for char in range(len(password_caesar)):
        k = key[char % m]
        if password_caesar[char].isupper():
            new_pass += chr((ord(password_caesar[char]) - 65 - ord(k)) % 26 + 65)
            continue
        if password_caesar[char].islower():
            new_pass += chr((ord(password_caesar[char]) - 97 - ord(k)) % 26 + 97)
            continue
        if password_caesar[char].isdigit():
            new_pass += str((int(password_caesar[char]) - ord(k)) % 10)
        else:
            new_pass += password_caesar[char]
    return new_pass


def decryption2_caesar(encr_pass, step=s):
    original_pass = ""
    for char in str(encr_pass):
        # if symbol is uppercased letter
        if char.isupper():
            original_pass += chr((ord(char) - step - 65) % 26 + 65)
            continue
        # ... if symbol is lowercased letter
        if char.islower():
            original_pass += chr((ord(char) - step - 97) % 26 + 97)
            continue
        if char.isdigit():
            original_pass += str((int(char) - step) % 10)
        # ... if symbol is special symbol, leave them
        else:
            original_pass += char
    return original_pass
