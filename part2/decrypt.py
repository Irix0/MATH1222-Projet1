import numpy as np
from numpy import inf
import random

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

# Create a dictionnary for the symbol counter, a dictionnary for theta and a dictrionnary for the transitions between symbols
def create_dictionnaries(symbols):
    symb_count = {}
    theta = {}
    transition_count = {}

    for i in symbols:
        symb_count[i] = 0
        theta[i] = i
        transition_count[i] = {}
        for j in symbols:
            transition_count[i][j] = 0
    return symb_count, theta, transition_count


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
def swap_theta(key1, key2, theta):
    new_theta = theta.copy()
    new_theta[key2] = theta[key1]
    new_theta[key1] = theta[key2]
    return new_theta

# Modify completely a susbtitution code by swapping each symbol to another one time
def modify_substitution_code(theta):
    for _ in range(len(theta)):
        key1, key2 = random.sample(list(theta), 2)
        theta = swap_theta(key1, key2, theta)
    return theta

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
def decrypt(string, theta):
    new_string = ""
    for i in range(len(string)):
        new_string += theta[string[i]]
    return new_string

# Determine the substitution code that has the best likelihood
def metropolis_hastings(string, theta, app_prob, trans_prob, nb_iter):
    likelihood = calculate_likelihood(string, app_prob, trans_prob)
    best_theta = [likelihood, theta]

    for _ in range(nb_iter):
        key1, key2 = random.sample(list(theta), 2)
        new_theta = swap_theta(key1, key2, theta)

        new_string = decrypt(string, new_theta)
        new_likelihood = calculate_likelihood(new_string, app_prob, trans_prob)

        alpha = min(0, new_likelihood - likelihood)

        if np.log(random.random()) < alpha:
            theta = new_theta
            likelihood = new_likelihood
            if best_theta[0] < likelihood:
                best_theta = [likelihood, theta]
    return best_theta

# Find the best substitution code
def find_susbtitution_code(crypted_string, theta, app_prob, trans_prob):
    likelihood = -inf
    best_theta = theta

    # Try 10 random theta to begin with and keep the code related to the best likelihood
    for _ in range(10):
        theta = modify_substitution_code(theta)
        new_string = decrypt(crypted_string, theta)
        new_likelihood = calculate_likelihood(new_string, app_prob, trans_prob)
        if new_likelihood > likelihood:
            likelihood = new_likelihood
            best_theta = theta

    # Try 10 different chains with the same begin point keep the best one and repeat it 10 times
    best_theta = [-inf, theta]
    for _ in range(10):
        theta = best_theta[1]
        for _ in range(10):
            new_theta = metropolis_hastings(crypted_string, theta, app_prob, trans_prob, 10000)
            if best_theta[0] < new_theta[0]:
                best_theta = new_theta
    return best_theta[1]

crypted_string = read_crypted_text("groupe-Louan_et_Van_de_Vyver-encryptedtext.txt")

symbols = symbols_reading("symbols.txt")
symb_count, theta, transition_count = create_dictionnaries(symbols)

app_prob, trans_prob = probabilities(symb_count, transition_count, "moby_dick.txt")

theta = find_susbtitution_code(crypted_string, theta, app_prob, trans_prob)
decrypted_string = decrypt(crypted_string, theta)

print(decrypted_string)
