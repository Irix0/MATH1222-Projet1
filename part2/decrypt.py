import math
import random

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

def probabilities(filename, char_count, transition_count):
    total_char = 0

    # Count the number of each symbols and their transitions by reading filename
    file = open(filename, "r")
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

# Create a new substitution by swapping key1 and key2
def create_new_theta(key1, key2, theta):
    new_theta = theta.copy()
    new_theta[key2] = theta[key1]
    new_theta[key1] = theta[key2]
    return new_theta

# Calculate the likelihood of a string
def calculate_likelihood(string, app_prob, trans_prob):
    likelihood = math.log(app_prob[string[0]])
    for i in range(len(string)-1):
        try :
            likelihood += math.log(trans_prob[string[i]][string[i+1]])
        except:
            likelihood += -100
    return likelihood

# Create a new string from another by using a substitution code
def decrypt(string, theta):
    new_string = ""
    for i in range(len(string)):
        new_string += theta[string[i]]
    return new_string

# Determine the substitution code that has the best likelihood
# Does not work
def metropolis_hastings(string, theta, app_prob, trans_prob, nb_iter):
    likelihood = calculate_likelihood(string, app_prob, trans_prob)

    i = 0
    while i < nb_iter:
        key1, key2 = random.sample(list(theta), 2)
        new_theta = create_new_theta(key1, key2, theta)

        new_string = decrypt(string, new_theta)
        new_likelihood = calculate_likelihood(new_string, app_prob, trans_prob)

        alpha = min(0, likelihood - new_likelihood)
        if likelihood < new_likelihood:
            theta = new_theta
            likelihood = new_likelihood
            print(likelihood)
        i += 1
    return theta

string1 = "wlenhenhjhnlm,whwznwhwz" + '"' + "whwmhdzhzsk,t;wz):"
print(string1)

symbols = symbols_reading("symbols.txt")
symb_count, theta, transition_count = create_dictionnaries(symbols)
app_prob, trans_prob = probabilities("moby_dick.txt", symb_count, transition_count)

theta = metropolis_hastings(string1, theta, app_prob, trans_prob, 1000000)
new_string = decrypt(string1, theta)

print(new_string)
