from decryption import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Create graphs to study the convergence of the algorithm
nb_iter = 5000
nb_jobs = 5

string = read_text("texts/text_2000_char.txt")

symbols = symbols_reading("texts/symbols.txt")
symb_count, code, transition_count = create_dictionnaries(symbols)

app_prob, trans_prob = probabilities(symb_count, transition_count, "texts/moby_dick.txt")

code = modify_substitution_code(code)
crypted_string = crypt(string, code)

for i in range(249, len(crypted_string), 250):
    delta_list = []
    uncrypted_likelihood = calculate_likelihood(string[:i], app_prob, trans_prob)

    likelihood_list = study_convergence(crypted_string[:i], code, app_prob, trans_prob, nb_jobs, nb_iter)

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Convergence de la vraisemblance", "Vraisemblance empirique"))

    for j in range(len(likelihood_list)):
        guesses = []

        best_guess = likelihood_list[j][0]
        percent = ((likelihood_list[j][0] - uncrypted_likelihood) / -uncrypted_likelihood) * 100
        for k in range(1,len(likelihood_list[j])):
            if likelihood_list[j][k] > best_guess:
                best_guess = likelihood_list[j][k]
                percent = ((likelihood_list[j][k] - uncrypted_likelihood) / -uncrypted_likelihood) * 100
            guesses.append(percent)
        fig.add_trace(go.Scatter(x=list(range(nb_iter)), y=guesses, name = 'Chaîne ' + str(j+1)), row=1, col=1)
        j += 1

    fig.add_trace(go.Scatter(x=list(range(nb_iter)), y=likelihood_list[0], name = 'Chaîne 1'), row=2, col=1)

    fig.add_trace(go.Scatter(x=list(range(nb_iter)), y=[uncrypted_likelihood]*nb_iter, name = 'Vraisemblance théorique', line=dict(dash='dash')), row=2, col=1)

    fig.update_xaxes(title_text="Nombre de répétitions")
    fig.update_yaxes(title_text="Pourcentage d'erreurs", row=1, col=1)
    fig.update_yaxes(title_text="Valeurs vraisemblances calculées", row=2, col=1)

    fig.update_layout(title_text="Évolution de la vraisemblance en fonction du nombre de répétitions de l'algorithme<br><sup>Longueur de la chaîne : {}</sup>".format(i+1))
    fig.show()