import math
import random

# Reads a file that contains all possible symbols and creates a list of them
def symbols_reading(filename):
    symbols = []
    
    file = open("characters.txt","r")
    symb = file.read(1)
    while symb:
        if symb != '\n':
            symbols.append(symb)
        symb = file.read(1)
    file.close()
    return symbols

# Create a dictionnary for the character counter, a dictionnary for theta and a dictrionnary for the transitions between symbols
def create_dictionnaries(symbols):
    char_count = {}
    theta = {}
    transition_count = {}

    for i in symbols:
        char_count[i] = 0
        theta[i] = i
        transition_count = {}
        for j in symbols:
            transition_count[i][j] = 0
    return char_count, theta, transition_count

def probabilities(filename):

    file = open(filename, "r")
    curr_char = file.read(1)
    next_char = file.read(1)
    while curr_char:
        if curr_char in char_count :
            char_count[curr_char] += 1
            if next_char in transition_count[curr_char]:
               transition_count[curr_char][next_char] += 1
        curr_char, next_char = next_char, file.read(1)

    # Calculate the apparition probabilities
    apparition_probabilities = {}
    total_char = 0
    for curr_char in char_count:
        total_char += char_count[curr_char]
    for curr_char in char_count:
        apparition_probabilities[curr_char] = char_count[curr_char] / total_char

    # Calculate the transition probabilities
    transition_probabilities = {}
    for curr_char in transition_count:
        transition_probabilities[curr_char] = {}
        for next_char in transition_count[curr_char]:
            transition_probabilities[curr_char][next_char] = transition_count[curr_char][next_char] / char_count[curr_char]

    file.close()
    return apparition_probabilities, transition_probabilities


def swap_theta(key1, key2, theta):
    tmp = theta[key1]
    theta[key1] = theta[key2]
    theta[key2] = tmp
    return theta

def calculate_likelihood(string, u, P):
    likelihood = math.log(u[string[0]])

    for i in range(len(string)-1):
        try :
            likelihood += math.log(P[string[i]][string[i+1]])
        except:
            likelihood = float('-inf')
    return likelihood

def decrypt(string, theta):
    new_string = ""
    for i in range(len(string)):
        new_string += theta[string[i]]
    return new_string

def metropolis_hastings(string, theta, u, P):
    return theta

symbols = symbols_reading("characters.txt")

string1 = "wlenhenhjhnlm,whwznwhwzwhwmhdzhzsk,t;wz):"

char_count, theta = characters_reading("characters.txt")
u, P = transition_probabilities("moby_dick.txt", char_count)

theta = metropolis_hastings(string1, theta, u, P)
new_string = decrypt(string1, theta)
