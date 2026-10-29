import csv
import matplotlib.pyplot as plt
import numpy as np

# coefficiente binomiale n k
def binomial(n, k):
    #no recursion
    if k == 0 or k == n:
        return 1
    if k == 1 or k == n-1:
        return n
    if k > n:
        return 0
    if k > n - k:
        k = n - k
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c

# fattoriale di n
def factorial(n):
    #no recursion
    tot = 1
    for i in range(1, n+1):
        tot = tot * i
    return tot

# probabilità di ottenere un tiro (considerato come combinazione, cioè non importa l'ordine). throws deve essere una lista di numeri da 1 a 6. Es. [4,3,6,1,2]
def p_esce_tiro(throws):
    count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for num in throws:
        count[num] = count[num] + 1
    probab = 1
    for i in range(len(throws)):
        probab *= i/6
    for val in count.values():
        probab //= factorial(val)
    return probab

# dato un attaccante con n_atk pedine e un difensore con n_atk pedine, restituisce un dizionario con le frequenze di ogni possibile esito.
# Per esempio, simulando un attaccante con 3 pedine e un difensore con 2 pedine, il dizionario restituito sarà {(2, 0): 2890, (1, 1): 2611, (0, 2): 2275}
# dove (2, 0) significa che il difensore ha perso 2 pedine e l'attaccante 2, e il numero associato è il numero di casi favorevoli.
# Tutti i casi possibili sono 6^(n_atk+n_dfn), ovvero tutti i possibili tiri di n_atk+n_dfn dadi a 6 facce. Di conseguenza per ottenere la probabilità
# di un certo esito basta dividere il numero associato all'esito per 6^(n_atk+n_dfn).
# Questa funzione funziona anche con n_atk e n_dfn maggiori di 3, ma è molto lenta per valori troppo alti. La complessità è O(6^(n_atk+n_dfn))
# e inizia ad essere estremamente lenta quando la somma di n_atk e n_dfn supera 9. Basti pensare che ogni volta che si aumenta di 1 la somma di n_atk e n_dfn
# l'algoritmo dura 6 volte di più del caso precedente
def lookup_table_risiko(n_atk, n_dfn):
    losses = min(n_atk, n_dfn)
    outcomes = {}
    for i in range(losses+1):
        outcomes[(losses-i, i)] = 0
    tot = n_atk + n_dfn
    for i in range(6**tot):
        throws = []
        for j in range(tot):
            throws.append((i)//(6**j)%(6))
        throws_atk = throws[:n_atk]
        throws_dfn = throws[n_atk:]
        throws_atk.sort(reverse=True)
        throws_dfn.sort(reverse=True)
        atk_loss = 0
        dfn_loss = 0
        for i in range(losses):
            if throws_atk[i] > throws_dfn[i]:
                dfn_loss += 1
            else:
                atk_loss += 1
        outcomes[(dfn_loss, atk_loss)] += 1
    return outcomes

# dato un attaccante con n_atk pedine e un difensore con n_atk pedine, restituisce un dizionario con le probabilità di ogni possibile esito. Se prob è True, 
# le probabilità sono espresse da 0 a 1, altrimenti sono espresse come numero di casi favorevoli, e in aggiunga c'è un campo "total" che indica il numero 
# totale di casi possibili. Qui l'unica differenza è che l'esito non è espresso come numero di pedine perse, ma numero di pedine rimanenti.
# Quindi per esempio outcome_risiko(3,2,prob=False) restituirà {(3, 0): 2890, (2, 1): 2611, (1, 2): 2275, 'total': 7776}
def outcome_risiko(n_atk, n_dfn, prob=True):
    table = lookup_table_risiko(n_atk, n_dfn)
    outcome = {}
    for key, value in table.items():
        if prob:
            outcome[(n_atk - key[1], n_dfn - key[0])] = value/(6**n_atk * 6**n_dfn)
        else:
            outcome[(n_atk - key[1], n_dfn - key[0])] = value
    if not prob:
        outcome["total"] = 6**n_atk * 6**n_dfn
    return outcome

# questa funzione calcola la probabilità che l'attaccante vinca un combattimento con n_atk pedine contro n_dfn pedine. La funzione è ricorsiva e utilizza una
# tabella per memorizzare le probabilità di ogni possibile esito. La complessità è O(n_atk*n_dfn) e quindi è molto più veloce di lookup_table_risiko per valori
# di n_atk e n_dfn superiori a 3. Calcolare il valore (n_atk, n_dfn) richiede la conoscenza delle probabilità dei casi da cui si può arrivare dopo una singola battaglia.
# La singola battaglia si intende come uno scontro 3v3, 3v2, 3v1, 2v3, 2v2, 2v1, 1v3, 1v2, 1v1. La formula è infatti la seguente:
# P(n_atk vs n_dfn vince atk) = Σ (per tutti i possibili outcome della prima battaglia) P(avviene quell'outcome) * P(n_atk - pedine perse vs n_dfn - pedine perse vince atk)
def atk_wins(n_atk, n_dfn, table = {}):
    outcome = outcome_risiko(min(n_atk, 3), min(n_dfn, 3), type="prob")
    probability = 0
    for out, prob in outcome.items():
        final_atk = n_atk - (min(n_atk, 3) - out[0])
        final_dfn = n_dfn - (min(n_dfn, 3) - out[1])
        # print("case from ", n_atk, n_dfn, " to ", final_atk, final_dfn, " with prob to happen ", prob, " and prob to atk win ", end="")
        if final_atk == 0:
            # print(0)
            continue
        elif final_dfn == 0:
            # print(1)
            probability += prob
        else:
            # print(table[(final_atk, final_dfn)])
            probability += prob * table[(final_atk, final_dfn)]
    table[n_atk, n_dfn] = probability
    return table

# crea un file csv con tutte le probabilità che l'attacco vinca con i pedine contro j pedine del difensore, con i e j che vanno da 0 a n (estremi inclusi).
# digits è il numero di cifre dopo la virgola usate per i numeri nel csv. Se verbose è True, allora verrà stampato a schermo il numero di riga e la percentuale
# di completamento corrente.
def create_risiko_csv(n, filename, digits=6, verbose=False):
    wins_table = {}
    for i in range(n+1):
        if verbose: print("row:", i, ", completion:", i/n*100, "%")
        for j in range(n+1):
            wins_table = atk_wins(i, j, wins_table)

    format_string = "{:.%df}" % digits
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(format_string.format(wins_table[(i, j)]))
        matrix.append(row)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

# crea un grafico a colori a partire da un file csv. digits è il numero di cifre dopo la virgola usate per i numeri nel csv. font è la dimensione del font
# usato per scrivere i numeri all'interno delle caselle. percentage indica se i numeri nel csv sono percentuali o meno. numbers indica se scrivere o meno
# i numeri all'interno delle caselle. dpi è la risoluzione del grafico.
def create_risiko_graph(filename, pic_name, digits=1, font=2, percentage=True, numbers=True, dpi=350):
    matrix = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append(row)

    n = len(matrix)

    format_string = "{:.%df}" % digits
    if percentage:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = format_string.format(float(matrix[i][j])*100)
                if matrix[i][j] == "100.0":
                    matrix[i][j] = "100"

    matrix = np.array(matrix)
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix.astype(float), cmap='coolwarm')
    fig.colorbar(cax)
    if numbers:
        for i in range(n):
            for j in range(n):
                ax.text(j, i, matrix[i, j], ha='center', va='center', fontsize=font)
    plt.savefig(pic_name+'.png', dpi=dpi)




###### ESEMPI ######

#### Esempio 1 #####
# crea un csv 100x100 con 6 cifre decimali e stampando il progresso a schermo
# create_risiko_csv(100, "Risiko100x100.csv", digits=6, verbose=True)

# crea un grafico a colori a partire da un file csv, usando 1 cifra decimale, fontsize 1, numeri percentuali e risoluzione 1200 dpi
# create_risiko_graph("Risiko100x100.csv", "Risiko100x100", digits=1, font=1, percentage=True, dpi=1200)



#### Esempio 2 #####
# crea un csv 1000x1000 con 10 cifre decimali e stampando il progresso a schermo
# create_risiko_csv(1000, "Risiko1000x1000.csv", digits=10, verbose=True)

# crea un grafico a colori a partire da un file csv, senza numeri all'interno delle caselle e risoluzione 1200 dpi
# create_risiko_graph("Risiko1000x1000.csv", "Risiko1000x1000", numbers=False, dpi=1200)



#### Esempio 3 #####
# stampa tutti i possibili outcome di un attacco con 3 pedine contro un difensore con 2 pedine come numero di casi favorevoli
print(outcome_risiko(3, 2, prob=False))



#### Esempio 4 #####
# leggi il csv della tabella 100x100 e trasformalo in una matrice di numeri
# matrix = []
# with open("Risiko100x100.csv", 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         matrix.append(row)
# matrix = np.array(matrix).astype(float)

# per ogni numero di attaccanti, calcola fino a che numero di difensori all'attaccante conviene attaccare (probabilità di vittoria >= 50%)
# for i in range(len(matrix)):
#     for j in range(len(matrix[i])-1, -1, -1):
#         if matrix[i, j] > 0.5:
#             print("atk:", i, "dfn:", j, "prob:", matrix[i, j])
#             break