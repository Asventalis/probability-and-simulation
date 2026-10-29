# Polish Poker Hand Probabilities

In "Polish poker" the number of cards in play changes, which reorders how likely each hand is. The script computes, for every n from 1 to 52 cards drawn from a 52-card deck, the probability of specific hands (high card, pair, two pair, three of a kind, straight, flush, full house, four of a kind, royal flush) with closed-form hypergeometric counts and inclusion-exclusion, prints the ranking of hands by probability for each n (`tabella.txt`), and checks the formulas against a Monte Carlo simulation.

## How to run
Python 3 with `matplotlib`: `python probabilities.py` prints the tables and shows the theoretical vs simulated curves.

## Notes
- The hands are defined in a specific way (e.g. "pair" means at least two aces, "flush" means at least five hearts), see the function docstrings; this is what the table reflects.
- Labels and output are in Italian.
