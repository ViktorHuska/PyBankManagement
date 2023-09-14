from encryption import encryption1_caesar, encryption2_vigenere

word = "Doug2023!"
word = encryption1_caesar(word)
word = encryption2_vigenere(word)

print(word)