import numpy as np
from numpy import inf
import random
from multiprocessing import Pool

# Read a cryptes text from a file
def read_crypted_text(filename):
    file = open(filename, "r")
    crypted_string = file.readline()
    return crypted_string

# Reads a file that contains all possible symbols and creates a list of them
def symbols_reading(filename):
    symbols = []

    file = open(filename,"r")
    symb = file.read(1)
    while symb:
        if symb != '\n' and symb not in symbols:
            symbols.append(symb)
        symb = file.read(1)
    file.close()
    return symbols

# Create a dictionnary for the symbol counter, a dictionnary for code and a dictrionnary for the transitions between symbols
def create_dictionnaries(symbols):
    symb_count = {}
    code = {}
    transition_count = {}

    for i in symbols:
        symb_count[i] = 0
        code[i] = i
        transition_count[i] = {}
        for j in symbols:
            transition_count[i][j] = 0
    return symb_count, code, transition_count

# Calculate the apparition probability of characters and the transition probabilities
def probabilities(char_count, transition_count, *filename):
    total_char = 0

    # Count the number of each symbols and their transitions by reading filename
    for i in range(len(filename)):
        file = open(filename[i])
        curr_char = file.read(1)
        next_char = file.read(1)
        while curr_char:
            if curr_char in char_count :
                char_count[curr_char] += 1
                if next_char in transition_count[curr_char]:
                    transition_count[curr_char][next_char] += 1
                total_char += 1
            curr_char, next_char = next_char, file.read(1)
        file.close()

    # Calculate the apparition probabilities and the transition probabilities
    apparition_probabilities = {}
    transition_probabilities = {}
    for curr_char in transition_count:
        apparition_probabilities[curr_char] = char_count[curr_char] / total_char
        transition_probabilities[curr_char] = {}
        for next_char in transition_count[curr_char]:
            transition_probabilities[curr_char][next_char] = transition_count[curr_char][next_char] / char_count[curr_char]

    return apparition_probabilities, transition_probabilities

# Create a new substitution code by swapping key1 and key2
def swap_code(key1, key2, code):
    new_code = code.copy()
    new_code[key2] = code[key1]
    new_code[key1] = code[key2]
    return new_code

# Modify completely a susbtitution code by swapping each symbol to another one time
def modify_substitution_code(code):
    for _ in range(len(code)):
        key1, key2 = random.sample(list(code), 2)
        code = swap_code(key1, key2, code)
    return code

# Calculate the likelihood of a string
def calculate_likelihood(string, app_prob, trans_prob):
    likelihood = np.log(app_prob[string[0]])
    for i in range(len(string)-1):
        if trans_prob[string[i]][string[i+1]] != 0.0:
            likelihood += np.log(trans_prob[string[i]][string[i+1]])
        else:
            likelihood += -10000
    return likelihood

# Create a new string from another by using a substitution code
def decrypt(string, code):
    new_string = ""
    for i in range(len(string)):
        new_string += code[string[i]]
    return new_string

# Determine the substitution code that has the best likelihood
def metropolis_hastings(args):
    string, code, app_prob, trans_prob, nb_iter, job = args
    likelihood = calculate_likelihood(string, app_prob, trans_prob)
    best_find = {'likelihood' : likelihood, 'code' : code}

    for _ in range(nb_iter):
        key1, key2 = random.sample(list(code), 2)
        new_code = swap_code(key1, key2, code)

        new_string = decrypt(string, new_code)
        new_likelihood = calculate_likelihood(new_string, app_prob, trans_prob)

        alpha = min(0, new_likelihood - likelihood)

        if np.log(random.random()) < alpha:
            code = new_code
            likelihood = new_likelihood
            if best_find['likelihood'] < likelihood:
                best_find['likelihood'] = likelihood
                best_find['code'] = code
    return best_find

# Multiprocess the instructions into different chains
def start_job(string, code, app_prob, trans_prob, nb_iter, n_jobs=10):
    jobs = []
    for _ in range(0, n_jobs):
        jobs.append((string, code, app_prob, trans_prob, nb_iter, _))

    finds = Pool(5).map(metropolis_hastings, jobs)
    best_find = {'likelihood' : -inf, 'code' : code}
    for find in finds:
        if find['likelihood'] > best_find['likelihood']:
            best_find = find
    return best_find

# Find the best substitution code
def find_susbtitution_code(crypted_string, code, app_prob, trans_prob):
    best_find = {'likelihood' : -inf, 'code' : code}

    # Try 10 random code to begin with and keep the code related to the best likelihood
    for _ in range(10):
        code = modify_substitution_code(code)
        new_string = decrypt(crypted_string, code)
        likelihood = calculate_likelihood(new_string, app_prob, trans_prob)
        if likelihood > best_find['likelihood']:
            best_find['likelihood'] = likelihood
            best_find['code'] = code

    # Keep the best substitution code found and repeat it nb_iter times
    nb_iter = 5
    print("Initializing decryption... (" + str(nb_iter) + " iterations)")
    for i in range(nb_iter):
        find = start_job(crypted_string, best_find['code'], app_prob, trans_prob, 10000)
        if find['likelihood'] > best_find['likelihood']:
            best_find = find
        print("Iteration " + str(i+1) + ". Best likelihood found: 10^(" + str(best_find['likelihood'])+ ")")

    print("Decryption finished")
    return best_find['code']


# Program to find the substitution code
crypted_string = read_crypted_text("groupe-Louan_et_Van_de_Vyver-encryptedtext.txt")

symbols = symbols_reading("symbols.txt")
symb_count, code, transition_count = create_dictionnaries(symbols)

app_prob, trans_prob = probabilities(symb_count, transition_count, "moby_dick.txt")

code = find_susbtitution_code(crypted_string, code, app_prob, trans_prob)
decrypted_string = decrypt(crypted_string, code)

print("\nBest susbtitution code found:")
print(code)

print("\nDecrypted text:")
print(decrypted_string)
