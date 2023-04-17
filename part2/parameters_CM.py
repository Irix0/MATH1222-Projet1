from locale import currency


def transition_probabilities(filename):
    char_count = {}
    transition_count = {}

    # Read a file that contains all possible characters that will be counted
    file = open("characters.txt","r")
    char = file.read(1)
    while char:
        if char != '\n':
            char_count[char] = 0
        char = file.read(1)
    file.close()

    # Create a list of all the possible transition and set them to 0
    for i in char_count:
        transition_count[i] = {}
        for j in char_count:
            transition_count[i][j] = 0

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
    print(apparition_probabilities)
    print(transition_probabilities)

    return


transition_probabilities("moby_dick.txt")