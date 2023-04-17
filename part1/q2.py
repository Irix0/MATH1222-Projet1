import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import math

def q(x, y, r):
    if x == 0 and y == 0:
        return r
    elif x == K and y == K:
        return 1-r
    elif 0 < x <= K and y == x-1:
        return r
    elif 0 <= x < K and y == x+1:
        return 1-r
    else:
        return 0
    
def combinational_probability(p, K, x):
    return math.comb(K, x)*(p**x)*((1-p)**(K-x))
    


def metropolis_hastings(p, K, r, n):
    # initialisation
    x = np.random.randint(0, K+1)
    samples = [x]
    
    for i in range(n):
        # proposition d'un nouvel état y
        if x == 0:
            y = np.random.choice([0,1], p=[1-r, r])
        elif x == K:
            y = np.random.choice([K-1, K], p=[r, 1-r])
        else:
            y = np.random.choice([x-1, x+1], p=[1-r, r])
    
        # Calculer le ratio de probabilité
        alpha = min(1, (combinational_probability(p, K, y) * q(x, y, r))) / (combinational_probability(p, K, x) * q(y, x, r))
    
        
        # décision d'acceptation ou de rejet
        u = np.random.uniform()
        if u < alpha:
            x = y
        
        samples.append(x)
    
    return samples

# paramètres de la loi
p = 0.3
K = 10

# paramètres de l'algorithme
n = 10000
rs = [0.1, 0.5]

fig_freq = go.Figure()

# boucle sur les différentes valeurs de r
for r in rs:
    samples = metropolis_hastings(p, K, r, n)
    
    # calcul de la moyenne et de la variance empiriques
    mean = np.mean(samples)
    var = np.var(samples)
    
    # calcul des valeurs théoriques de la moyenne et de la variance
    theoretical_mean = p * K
    theoretical_var = p * (1 - p) * K
    
    # affichage des résultats
    print("r = {}, n = {}".format(r, n))
    print("Moyenne empirique : {:.4f}".format(mean))
    print("Moyenne théorique : {:.4f}".format(theoretical_mean))
    print("Variance empirique : {:.4f}".format(var))
    print("Variance théorique : {:.4f}".format(theoretical_var))
    print()
    
    # affichage de l'évolution de la moyenne et de la variance en fonction de la longueur de l'échantillon
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Evolution de la moyenne", "Evolution de la variance"))

    # ajout des traces au premier sous-graphique
    fig.add_trace(go.Scatter(x=list(range(n+1)), y=np.cumsum(samples)/(np.arange(n+1)+1), name='Moyenne empirique'), row=1, col=1)
    fig.add_trace(go.Scatter(x=list(range(n+1)), y=[theoretical_mean]*(n+1), name='Moyenne théorique', line=dict(dash='dash')), row=1, col=1)
    fig.update_xaxes(title_text="Longueur de l'échantillon", row=1, col=1)
    fig.update_yaxes(title_text="Moyenne empirique", row=1, col=1)

    # ajout des traces au second sous-graphique
    fig.add_trace(go.Scatter(x=list(range(n+1)), y=np.cumsum((samples-mean)**2)/(np.arange(n+1)+1), name='Variance empirique'), row=2, col=1)
    fig.add_trace(go.Scatter(x=list(range(n+1)), y=[theoretical_var]*(n+1), name='Variance théorique', line=dict(dash='dash')), row=2, col=1)
    fig.update_xaxes(title_text="Longueur de l'échantillon", row=2, col=1)
    fig.update_yaxes(title_text="Variance empirique", row=2, col=1)

    # ajout d'un titre au graphique
    fig.update_layout(title_text="Convergence de la moyenne et de la variance<br><sup>Paramètres : p = {}, K = {}, r = {}, n = {}</sup>".format(p, K, r, n))
    #fig.show()

    # Récupérrez les fréquences d'apparition de chaque valeur de x
    x, counts = np.unique(samples, return_counts=True)
    # Calculer la probabilité empirique de chaque valeur de x
    freq = counts / n
    # Créer un histogramme avec plotly
    fig_freq.add_trace(go.Bar(x=x, y=freq, name="r = {}".format(r)))
    

# Fréquence théorique
freq_theo = [combinational_probability(p, K, x_i) for x_i in x]
print(freq_theo)
# Ajouter la fréquence théorique au graphique
fig_freq.add_trace(go.Scatter(x=x, y=freq_theo, name="théorique".format(r), line=dict(dash='dash')))   
fig_freq.update_layout(title_text="Histogramme des fréquences d'apparition des valeurs de x<br><sup>Paramètres : p = {}, K = {}, n = {}</sup>".format(p, K, n), xaxis=dict(title='Valeur', tickmode='linear'), yaxis=dict(title="Fréquence d'apparition"))
fig_freq.show()