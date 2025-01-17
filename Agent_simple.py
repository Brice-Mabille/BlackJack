import Jeu_regles
from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

class SimpleBlackjackAgent:
    def __init__(self):
        pass
    
    def choose_action(self, hand_value):
        """
        Choisit l'action à faire en fonction de la somme des cartes du joueur.
        """        
        # Si la somme des cartes est inférieure à 17, l'agent choisit de tirer.
        if hand_value < 17:
            return 'h'  # Tirer
        else:
            return 's'  # S'arrêter


# Définir l'agent avec une stratégie simple
def agent_turn(player_hand, deck, hand):
    agent = SimpleBlackjackAgent()  # Créer l'agent
    while player_hand.value < 21:  # Tant que la valeur des cartes du joueur est inférieure ou égale à 21
        action = agent.choose_action(player_hand.value)  # Choisir l'action selon la stratégie de l'agent
        if action == 'h':  # Si l'agent choisit de tirer
            hit(deck, player_hand)  # Tirer une carte
        else:  # Si l'agent choisit de s'arrêter
            break  # L'agent arrête de jouer
    return player_hand  # Retourner la valeur finale de la main de l'agent