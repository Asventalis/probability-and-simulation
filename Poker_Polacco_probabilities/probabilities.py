from matplotlib import pyplot as plt

#
def comb(n, k):
    if k > n or k < 0:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)  # Take advantage of symmetry
    c = 1
    for i in range(k):
        c = c * (n - i) / (i + 1)
    return c

def p_carta_alta(n):
    return 1 - comb(48, n) / comb(52, n)

def p_coppia(n):
    return p_carta_alta(n) - 4 * comb(48, n-1) / comb(52, n) if n >= 2 else 0

def p_doppia_coppia(n):
    if n < 4:
        return 0.0  # impossibile avere 2+2 carte
    
    total = comb(52, n)
    favorable = 0

    # a = numero di carte del primo valore (A)
    # b = numero di carte del secondo valore (B)
    for a in range(2, min(4, n) + 1):
        for b in range(2, min(4, n - a) + 1):
            favorable += comb(4, a) * comb(4, b) * comb(44, n - a - b)

    return favorable / total

def p_tris(n):
    return p_coppia(n) - 6 * comb(48, n-2) / comb(52, n) if n >= 3 else 0

def p_scala(n):
    if n < 5:
        return 0.0

    total = comb(52, n)
    values = 5  # 10,J,Q,K,A

    prob = 0
    for k in range(0, values + 1):
        remaining_cards = 52 - 4*k
        if remaining_cards >= n:
            term = comb(values, k) * comb(remaining_cards, n)
            prob += (-1)**k * term

    return prob / total

def p_colore(n):
    """
    Probabilità di avere almeno 5 cuori tra n carte pescate da un mazzo di 52.
    """
    total = comb(52, n)
    prob = 0

    for h in range(5, min(13, n) + 1):
        prob += comb(13, h) * comb(39, n - h)

    return prob / total

def p_poker(n):
    return comb(48, n-4) / comb(52, n) if n >= 4 else 0

def p_full(n):
    """
    Probabilità di avere almeno 3 assi e almeno 2 re tra n carte.
    (Full specifico: tris di assi + doppia di re)
    """
    total = comb(52, n)
    favorable = 0

    # a = numero di assi
    # b = numero di re
    for a in range(3, min(4, n) + 1):
        for b in range(2, min(4, n - a) + 1):
            favorable += comb(4, a) * comb(4, b) * comb(44, n - a - b)

    return favorable / total

def p_scala_reale(n):
    """
    Probabilità di avere la scala reale di cuori (10♥ J♥ Q♥ K♥ A♥)
    tra n carte pescate da un mazzo di 52 carte.
    """
    if n < 5:
        return 0.0

    return comb(47, n-5) / comb(52, n)

# graph all p_carta_alta from n=1 to n=52
n_values = list(range(1, 53))
carta_alta_values = [p_carta_alta(n) for n in n_values]
coppia_values = [p_coppia(n) for n in n_values]
doppia_coppia_values = [p_doppia_coppia(n) for n in n_values]
tris_values = [p_tris(n) for n in n_values]
scala_values = [p_scala(n) for n in n_values]
colore_values = [p_colore(n) for n in n_values]
full_values = [p_full(n) for n in n_values]
poker_values = [p_poker(n) for n in n_values]
scala_reale_values = [p_scala_reale(n) for n in n_values]


plt.plot(n_values, carta_alta_values, label='Carta Alta')
plt.plot(n_values, coppia_values, label='Coppia')
plt.plot(n_values, doppia_coppia_values, label='Doppia Coppia')
plt.plot(n_values, tris_values, label='Tris')
plt.plot(n_values, scala_values, label='Scala')
plt.plot(n_values, colore_values, label='Colore')
plt.plot(n_values, full_values, label='Full')
plt.plot(n_values, poker_values, label='Poker')
plt.plot(n_values, scala_reale_values, label='Scala Reale')
plt.legend()
plt.xlabel('Numero di carte in gioco (n)')
plt.ylabel('Pronabilità')
plt.title('Probabilità di ogni mano in n carte')
plt.grid(True)
plt.show()

# adesso, per ogni n da 1 a 52, crea un dict delle mani ordinate per probabilità decrescente
# dopodiche, usalo per stampare una tabella che per ogni n ti dice l'ordine delle mani per probabilità
hand_probabilities = {}
for n in range(1, 53):
    hand_probabilities[n] = {
        'Carta Alta': p_carta_alta(n),
        'Coppia': p_coppia(n),
        'Doppia Coppia': p_doppia_coppia(n),
        'Tris': p_tris(n),
        'Scala': p_scala(n),
        'Colore': p_colore(n),
        'Full': p_full(n),
        'Poker': p_poker(n),
        'Scala Reale': p_scala_reale(n)
    }

    # ordina il dict per probabilità decrescente
    hand_probabilities[n] = dict(sorted(hand_probabilities[n].items(), key=lambda item: item[1], reverse=True))
    print(f"{n}", end="")
    stringa = ""
    for hand, prob in hand_probabilities[n].items():
        stringa += f",{hand}"
    print(stringa)

# make a montecarlo simulation for each n to count all the hands present K samples
import random
K = 1000
montecarlo_results = {}

for n in range(1, 53):
    counts = {
        'Carta Alta': 0,
        'Coppia': 0,
        'Doppia Coppia': 0,
        'Tris': 0,
        'Scala': 0,
        'Colore': 0,
        'Full': 0,
        'Poker': 0,
        'Scala Reale': 0
    }

    deck = [f"{rank}{suit}" for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] for suit in ['H', 'D', 'C', 'S']]
    carta_alta = ['A']
    coppia = ['A', 'A']
    doppia_coppia = ['A', 'A', 'K', 'K']
    tris = ['A', 'A', 'A']
    scala = ['10', 'J', 'Q', 'K', 'A']
    colore = ['H'] * 5
    full = ['A', 'A', 'A', 'K', 'K']
    poker = ['A', 'A', 'A', 'A']
    scala_reale = ['10H', 'JH', 'QH', 'KH', 'AH']

    for _ in range(K):
        # with no replacement
        hand = random.sample(deck, n)
        suits = [card[-1] for card in hand]
        ranks = [card[:-1] for card in hand]

        if carta_alta[0] in ranks:
            counts['Carta Alta'] += 1
        if ranks.count('A') >= 2:
            counts['Coppia'] += 1
        if ranks.count('A') >= 2 and ranks.count('K') >= 2:
            counts['Doppia Coppia'] += 1
        if ranks.count('A') >= 3:
            counts['Tris'] += 1
        if all(rank in ranks for rank in ['10', 'J', 'Q', 'K', 'A']):
            counts['Scala'] += 1
        if suits.count('H') >= 5:
            counts['Colore'] += 1
        if ranks.count('A') >= 3 and ranks.count('K') >= 2:
            counts['Full'] += 1
        if ranks.count('A') >= 4:
            counts['Poker'] += 1
        if all(card in hand for card in ['10H', 'JH', 'QH', 'KH', 'AH']):
            counts['Scala Reale'] += 1
    montecarlo_results[n] = {hand: counts[hand] / K for hand in counts}
    print(f"Montecarlo n={n}: ", end="")
    for hand, prob in montecarlo_results[n].items():
        print(f",{hand}:{prob:.6f}", end="")
    print()

# make graphs
for hand in ['Carta Alta', 'Coppia', 'Doppia Coppia', 'Tris', 'Scala', 'Colore', 'Full', 'Poker', 'Scala Reale']:
    theoretical = [hand_probabilities[n][hand] for n in range(1, 53)]
    montecarlo = [montecarlo_results[n][hand] for n in range(1, 53)]

    plt.plot(n_values, theoretical, label=f'Teorica {hand}')
    plt.plot(n_values, montecarlo, label=f'Montecarlo {hand}', linestyle='dashed')
    plt.xlabel('Numero di carte in gioco (n)')
    plt.ylabel('Probabilità')
    plt.title(f'Probabilità di {hand} in n carte')
    plt.legend()
    plt.grid(True)
    plt.show()