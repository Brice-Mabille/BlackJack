import random
import time
import numpy as np
import Jeu_regles
import Agent_Q_learning

from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push
from Agent_Q_learning import train_q_learning_agent

playing = True

# Entraînement de l'agent
trained_agent, scores, final_hands = train_q_learning_agent(episodes=100)

print(f"")

# Exemple d'utilisation de l'agent
print("\nAgent training complete. Testing the trained agent...")

print("\n----------------------------------------------------------------")
print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
print("                          Lets Play!")
print("----------------------------------------------------------------")

for _ in range(5):
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    has_ace = player_hand.aces > 0
    dealer_card = Card.values[dealer_hand.cards[0].rank]
    state = trained_agent.get_state(player_hand.value, has_ace, dealer_card)

    while player_hand.value <= 21:
        action = trained_agent.q_learning_choose_action(state)
 
        if action == 'h':
            hit(deck, player_hand)
        else:
            break
    
    if player_hand.value > 21:
        player_busts(player_hand, dealer_hand)
    else:
        # Tour du dealer
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

    show_all(player_hand, dealer_hand)
    
    if dealer_hand.value > 21:
        dealer_busts(player_hand, dealer_hand)
    elif dealer_hand.value > player_hand.value or player_hand.value > 21:
        dealer_wins(player_hand, dealer_hand)
    elif dealer_hand.value < player_hand.value and player_hand.value <=21:
        player_wins(player_hand, dealer_hand)
    else:
        push(player_hand, dealer_hand)

    time.sleep(1)
    print("\n----------------------------------------------------------------")
    print("                     ★ Final Results ★")
    print("----------------------------------------------------------------")