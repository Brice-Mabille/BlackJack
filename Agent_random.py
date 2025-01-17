import random
from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

class RandomBlackjackAgent:
    def __init__(self):
        pass

def random_agent_turn(player_hand, deck, hand):
    agent = RandomBlackjackAgent()  # Créer l'agent aléatoire
    while player_hand.value < 32:  # Tant que la valeur des cartes du joueur est inférieure ou égale à 21
        action = random.choice(['h', 's'])  # Choisir une action aléatoire

        if action == 'h':  # Si l'agent choisit de tirer
            hit(deck, player_hand)  # Tirer une carte
            if player_hand.value > 32 :  # Si l'agent dépasse 21
                break
        else:  # Si l'agent choisit de s'arrêter
            break  # L'agent arrête de jouer
    return player_hand  # Retourner la valeur finale de la main de l'agent
