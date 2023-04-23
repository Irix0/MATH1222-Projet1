# Program to find the substitution code of an encrypted text

from decryption import *

crypted_string = read_text("texts/groupe-Louan_et_Van_de_Vyver-encryptedtext_20_04_2023.txt")

symbols = symbols_reading("texts/symbols.txt")
symb_count, code, transition_count = create_dictionnaries(symbols)

app_prob, trans_prob = probabilities(symb_count, transition_count, "texts/moby_dick.txt")

code = find_susbtitution_code(crypted_string, code, app_prob, trans_prob)
decrypted_string = decrypt(crypted_string, code)

print("\nBest susbtitution code found:")
print(code)

print("\nDecrypted text:")
print(decrypted_string)

original_text = read_text("texts/perfect_decryption.txt")
print("\nPerfect decryption likelihood: 10^(" + str(calculate_likelihood(original_text, app_prob, trans_prob)) + ")")