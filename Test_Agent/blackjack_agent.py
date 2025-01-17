########################################################## Blackjack ###########################################################
# -*- coding: utf-8 -*-
# Submitted by : Sheetal Bongale
# Python script simulates a simple command-line Blackjack game implemented using Python and Object Oriented Programming concepts
# System Requirements: Python 3.8 (Python3)
################################################################################################################################

import random
import time
import numpy as np
import Jeu_regles
import Agent_simple
import Agent_random
import Agent_Q_learning

from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push
from Agent_simple import agent_turn
from Agent_random import random_agent_turn
from Agent_Q_learning import train_q_learning_agent

playing = True

#Main

while True:
    print("\n----------------------------------------------------------------")
    print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
    print("                          Lets Play!")
    print("----------------------------------------------------------------")

    # Créer et mélanger le deck, distribuer deux cartes à chaque joueur
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Afficher les cartes
    show_some(player_hand, dealer_hand)

    # Tour de l'agent
    print("\nAgent's turn...")
    agent_hand_value = agent_turn(deck, player_hand)  # Agent avec condition += 17 -> Arrêt
    #agent_hand_value = random_agent_turn(deck, player_hand)  # Agent aléatoire

    # Vérifier si l'agent a busté
    if agent_hand_value > 21:
        player_busts(player_hand, dealer_hand)
    else:
        # Tour du dealer
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            time.sleep(1)
            print("\n----------------------------------------------------------------")
            print("                     ★ Final Results ★")
            print("----------------------------------------------------------------")

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand)
            else:
                push(player_hand, dealer_hand)

    # Demander si on veut jouer une autre main
    new_game = input("\nPlay another hand? [Y/N] ")
    while new_game.lower() not in ["y", "n"]:
        new_game = input("Invalid Input. Please enter 'y' or 'n' ")
    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("\n------------------------Thanks for playing!---------------------\n")
        break
    
