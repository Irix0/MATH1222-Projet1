import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

input_str = "abbbabcabcbcbdababbcacacbdacbacbbbdabdabbabacabbabdabdacbababbcacbabcbcacbcbabdacbbbbacbabbdacababcacbdabbbacbdacbcbdacbdababcbdacbabacabcabcbcababbcbababbcabcbdacbcacbdacbdacacabbdacabdabbababcababbdabcbabbabcabcbababbabbdacabbbdabbbabacabacacbbdabdabcbbbcabbdacabababbbbcbdabdacabdacabbbabacacbbbdacabcbdabcbacbbcbbbacacabbdababcbbcbbdacbdacabdacbababcacbdacbabdabbbacbababbdababbcacbcabdabdabcbdacbbdacbcbbbabdabbbbcabcbcbdabbcbabbabacabdabacbbabbcbdababacabcabbabdacbdababdabcacbbabacbabdabcabdac"

def transition_probabilities(input_str):
    char_count = {}
    transition_count = {}
    for i in range(len(input_str)-1):
        curr_char, next_char = input_str[i], input_str[i+1]
        if curr_char not in char_count:
            char_count[curr_char] = 0
        char_count[curr_char] += 1
        if curr_char not in transition_count:
            transition_count[curr_char] = {}
        if next_char not in transition_count[curr_char]:
            transition_count[curr_char][next_char] = 0
        transition_count[curr_char][next_char] += 1

    # Calculate the transition probabilities
    transition_probabilities = {}
    for curr_char in transition_count:
        transition_probabilities[curr_char] = {}
        for next_char in transition_count[curr_char]:
            transition_probabilities[curr_char][next_char] = transition_count[curr_char][next_char] / char_count[curr_char]

    # Convert the transition probabilities to a numpy array
    return np.array([[transition_probabilities.get(curr_char, {}).get(next_char, 0) for next_char in ['a', 'b', 'c', 'd']] for curr_char in ['a', 'b', 'c', 'd']])

def compute_probabilities(P, n):
    # Taille de la matrice de transition
    size = P.shape[0]
    # Distribution de probabilité uniforme initiale
    p0 = np.ones(size) / size

    # Probabilité de Xn = x pour une distribution initiale uniforme
    px_uniform = np.zeros((n+1, size))
    px_uniform[0] = p0
    for i in range(1, n+1):
        px_uniform[i] = px_uniform[i-1] @ P

    # Probabilité de Xn = x pour un état initial c fixé
    c_index = 2 # l'indice de l'état c dans la liste a,b,c,d
    px_c = np.zeros((n+1, size))
    px_c[0][c_index] = 1
    for i in range(1, n+1):
        px_c[i] = px_c[i-1] @ P

    # Matrice de transition à la puissance n
    P_n = np.linalg.matrix_power(P, n)

    return px_uniform, px_c, P_n

def random_realization(P, pi, T):
    # Initialisation de la réalisation aléatoire avec la distribution stationnaire
    realization = [np.random.choice(len(pi), p=pi)]
    
    # Génération de la réalisation aléatoire
    for i in range(T-1):
        realization.append(np.random.choice(len(pi), p=P[realization[-1], :]))
    
    # Convertit les indices en lettres
    letters = ['a', 'b', 'c', 'd']
    realization = [letters[index] for index in realization]
    
    return realization


p = transition_probabilities(input_str)
print("Matrice de transition :")
print(p)

px_uniform, px_c, P_n = compute_probabilities(p, 8)

MARKERS_SIZE = 15
# Create a figure for the uniform plot
fig_uniform = go.Figure()
fig_uniform.add_trace(go.Scatter(x=list(range(len(px_uniform[:,0]))), y=px_uniform[:,0], mode='markers', marker=dict(symbol='circle', size=MARKERS_SIZE), name='a'))
fig_uniform.add_trace(go.Scatter(x=list(range(len(px_uniform[:,1]))), y=px_uniform[:,1], mode='markers', marker=dict(symbol='square', size=MARKERS_SIZE), name='b'))
fig_uniform.add_trace(go.Scatter(x=list(range(len(px_uniform[:,2]))), y=px_uniform[:,2], mode='markers', marker=dict(symbol='diamond', size=MARKERS_SIZE), name='c'))
fig_uniform.add_trace(go.Scatter(x=list(range(len(px_uniform[:,3]))), y=px_uniform[:,3], mode='markers', marker=dict(symbol='cross', size=MARKERS_SIZE), name='d'))
fig_uniform.update_layout(title="Probabilité de transition uniforme",
                          xaxis_title=r'$n$',
                          yaxis_title=r"$\mathbb{P}(X_n = x)$",
                          legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='rgba(0, 0, 0, 0)'))

# Create a figure for the c plot
fig_c = go.Figure()
fig_c.add_trace(go.Scatter(x=list(range(len(px_c[:,0]))), y=px_c[:,0], mode='markers', marker=dict(symbol='circle', size=MARKERS_SIZE), name='a'))
fig_c.add_trace(go.Scatter(x=list(range(len(px_c[:,1]))), y=px_c[:,1], mode='markers', marker=dict(symbol='square', size=MARKERS_SIZE), name='b'))
fig_c.add_trace(go.Scatter(x=list(range(len(px_c[:,2]))), y=px_c[:,2], mode='markers', marker=dict(symbol='diamond', size=MARKERS_SIZE), name='c'))
fig_c.add_trace(go.Scatter(x=list(range(len(px_c[:,3]))), y=px_c[:,3], mode='markers', marker=dict(symbol='cross', size=MARKERS_SIZE), name='d'))
fig_c.update_layout(title="Probabilité de transition avec état initial c",
                    xaxis_title=r'$n$',
                    yaxis_title=r"$\mathbb{P}(X_n = x)$",
                    legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='rgba(0, 0, 0, 0)'))

# Show the figures
fig_uniform.show()
fig_c.show()

#print("Matrice de transition à la puissance n:")
#print(P_n)

counts = []

for i in range(50, 10000, 50):
    realization = random_realization(p, np.array([0.39583333, 0.27777778, 0.20833333, 0.11805556]), i)
    counts.append({letter: realization.count(letter)/len(realization) for letter in set(realization)}) 

# Créer un graphique en barres pour afficher les fréquences de chaque lettre
fig = go.Figure()
for letter in set(realization):
    fig.add_trace(go.Scatter(x=list(range(0, 500000, 10000)), y=[c.get(letter, 0) for c in counts], name=letter, legendrank=ord(letter)))

# Mettre en forme le graphique
fig.update_layout(title='Fréquences des lettres dans la réalisation aléatoire',
                  xaxis_title='Longueur de la réalisation',
                  yaxis_title='Fréquence',
                  legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='rgba(0, 0, 0, 0)'))
fig.show()
