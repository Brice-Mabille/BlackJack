import matplotlib.pyplot as plt
import numpy as np
import random
from carte_jeu import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push
from Q_learning import train_q_learning_agent
from Sarsa import train_sarsa_agent

# Fonction pour tester les agents
def test_agent(agent, episodes):
    """
    Teste les performances d'un agent sur un nombre défini d'épisodes.
    Renvoie le pourcentage de victoires, égalités et défaites.
    """
    wins = [0]

    for i in range(episodes):
        
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Tour de l'agent
        player_hand = agent(player_hand, deck, dealer_hand)

        # Tour du dealer
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Comparer les mains
        
        if player_hand.value > 21:  # Joueur a perdu
            wins.append(wins[-1])
        elif dealer_hand.value > 21:  # Dealer a perdu
            wins.append(wins[-1] + 1)
        elif player_hand.value > dealer_hand.value:  # Joueur gagne
            wins.append(wins[-1] + 1)
        elif player_hand.value < dealer_hand.value:  # Dealer gagne
            wins.append(wins[-1])
        else:  # Égalité
            wins.append(wins[-1])

    return wins


# Agents à tester
def simple_agent(player_hand, deck, dealer_hand):
    while player_hand.value < 17:  # Règle simple : hit si < 17
        hit(deck, player_hand)
    return player_hand


# Entraînement de l'agent Q-Learning
trained_q_learning_agent = train_q_learning_agent(episodes=10000)
trained_sarsa_agent = train_sarsa_agent(episodes=10000)

def q_learning_agent(player_hand, deck, dealer_hand):
    has_ace = player_hand.aces > 0
    dealer_card = dealer_hand.cards[0].values
    state = trained_q_learning_agent.get_state(player_hand.value, has_ace, dealer_card)

    while player_hand.value <= 21:
        action = trained_q_learning_agent.q_learning_choose_action(state)
        if action == 'h':  # Hit
            hit(deck, player_hand)
        else:  # Stand
            break
        has_ace = player_hand.aces > 0
        state = trained_q_learning_agent.get_state(player_hand.value, has_ace, dealer_card)
    return player_hand

def SARSA_agent(player_hand, deck, dealer_hand):
    has_ace = player_hand.aces > 0
    #dealer_card = dealer_hand.cards[0].values
    dealer_card = Card.values[dealer_hand.cards[0].rank]

    state = trained_sarsa_agent.get_state(player_hand.value, has_ace, dealer_card)

    while player_hand.value <= 21:
        action = trained_sarsa_agent.sarsa_choose_action(state)
        if action == 'h':  # Hit
            hit(deck, player_hand)
            if player_hand.value > 21:  # Joueur dépasse 21
                break
            # Mettre à jour l'état après le hit
            has_ace = player_hand.aces > 0
            state = trained_sarsa_agent.get_state(player_hand.value, has_ace, dealer_card)
        else:  # Stand
            break
    return player_hand

# Comparaison des performances
episodes = 30
simple_wins = test_agent(simple_agent, episodes)
q_learning_wins = test_agent(q_learning_agent, episodes)
sarsa_wins = test_agent(SARSA_agent, episodes)

# Tracer les courbes
plt.figure()
plt.plot(range(0, episodes+1),simple_wins, label="Simple Agent", color="blue")
plt.plot(range(0, episodes+1),q_learning_wins, label="Q-Learning Agent", color="green")
plt.plot(range(0, episodes+1),sarsa_wins, label="SARSA Agent", color="orange")
plt.xlabel("Nombre d'épisodes")
plt.ylabel("Taux de victoires")
plt.title("Comparaison des performances entre Simple Agent et Q-Learning Agent")
plt.legend()
plt.grid()
plt.show()
