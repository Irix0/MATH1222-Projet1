from decryption import *

string = read_text("texts/text_2000_char.txt")

symbols = symbols_reading("texts/symbols.txt")
symb_count, code, transition_count = create_dictionnaries(symbols)

app_prob, trans_prob = probabilities(symb_count, transition_count, "texts/moby_dick.txt")

code = modify_substitution_code(code)
crypted_string = crypt(string, code)

for i in range(0, len(string), 200)
    