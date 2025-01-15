import random

class RandomBlackjackAgent:
    def __init__(self):
        pass

    def random_action(self):
        """
        Choisit une action aléatoire : tirer ('h') ou rester ('s').
        """
        return random.choice(['h', 's'])


def random_agent_turn(deck, hand):
    agent = RandomBlackjackAgent()  # Créer l'agent aléatoire
    while hand.value < 21:  # Tant que la valeur des cartes du joueur est inférieure ou égale à 21
        action = agent.random_action()  # Choisir une action aléatoire

        if action == 'h':  # Si l'agent choisit de tirer
            hit(deck, hand)  # Tirer une carte
            print(f"Random Agent hits: {hand.cards[-1]} | New hand value: {hand.value}")
        else:  # Si l'agent choisit de s'arrêter
            print(f"Random Agent stands with hand: {hand.cards} | Hand value: {hand.value}")
            break  # L'agent arrête de jouer
    return hand.value  # Retourner la valeur finale de la main de l'agent
