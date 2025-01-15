import carte_jeu
from carte_jeu import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

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
def agent_turn(deck, hand):
    agent = SimpleBlackjackAgent()  # Créer l'agent
    while hand.value < 21:  # Tant que la valeur des cartes du joueur est inférieure ou égale à 21
        action = agent.choose_action(hand.value)  # Choisir l'action selon la stratégie de l'agent

        if action == 'h':  # Si l'agent choisit de tirer
            hit(deck, hand)  # Tirer une carte
            print(f"Agent hits: {hand.cards[-1]} | New hand value: {hand.value}")
        else:  # Si l'agent choisit de s'arrêter
            print(f"Agent stands with hand: {hand.cards} | Hand value: {hand.value}")
            break  # L'agent arrête de jouer
    return hand.value  # Retourner la valeur finale de la main de l'agent