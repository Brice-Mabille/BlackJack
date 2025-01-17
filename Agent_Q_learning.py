import random
import numpy as np 
import Jeu_regles
from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

class QLearningBlackjackAgent:
        # Configuration des hyperparamètres du Q-Learning
    ALPHA = 0.1  # Taux d'apprentissage
    GAMMA = 0.95  # Facteur de décroissance de la récompense future
    EPSILON = 1.0  # Équilibre exploration/exploitation (initialement 100% exploration)
    EPSILON_DECAY = 0.9  # Facteur de décroissance d'EPSILON
    EPSILON_MIN = 0.2  # Valeur minimum d'EPSILON

    # Actions possibles
    ACTIONS = ['h', 's']  # 'h' : Hit, 's' : Stand
    def __init__(self):
        # La table Q est un dictionnaire dont les clés sont les états et les valeurs sont les actions
        self.q_table = {}

    def get_state(self, hand_value, has_ace, dealer_card):
        """
        Représente l'état comme un tuple : (somme des cartes, as utilisable, carte visible du dealer)
        """
        return (hand_value, has_ace, dealer_card)

    def q_learning_choose_action(self, state):
        """
        Choisit une action selon une stratégie epsilon-greedy
        """
        if random.random() < QLearningBlackjackAgent.EPSILON:
            return random.choice(QLearningBlackjackAgent.ACTIONS)  # Exploration : action aléatoire
        else:
            if state not in self.q_table:
                self.q_table[state] = [0, 0]  # Initialiser les valeurs Q si l'état est inconnu
            return QLearningBlackjackAgent.ACTIONS[np.argmax(self.q_table[state])]  # Exploitation : action avec meilleure valeur Q

    def update_q_value(self, state, action, reward, next_state):
        """
        Met à jour la valeur Q en utilisant la formule de Q-Learning
        """
        if state not in self.q_table:
            self.q_table[state] = [0, 0]  # Initialiser les valeurs Q pour un état inconnu

        if next_state not in self.q_table:
            self.q_table[next_state] = [0, 0]  # Initialiser les valeurs Q pour l'état suivant inconnu

        action_idx = QLearningBlackjackAgent.ACTIONS.index(action)
        max_next_q = max(self.q_table[next_state])
        current_q = self.q_table[state][action_idx]

        # Mise à jour de la valeur Q
        self.q_table[state][action_idx] = current_q + QLearningBlackjackAgent.ALPHA * (reward + QLearningBlackjackAgent.GAMMA * max_next_q - current_q)

# Fonction pour l'entraînement de l'agent
def train_q_learning_agent(episodes):

    agent = QLearningBlackjackAgent()
    scores = []  # Liste pour stocker les scores moyens
    final_hands = []  # Liste pour stocker les mains finales moyennes

    for episode in range(episodes):
        # Initialiser un nouvel épisode
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Déterminer si le joueur a un as utilisable
        has_ace = player_hand.aces > 0
        dealer_card = Card.values[dealer_hand.cards[0].rank]
        state = agent.get_state(player_hand.value, has_ace, dealer_card)
        
        total_reward = 0
        actions_taken = []

        # Jouer le tour du joueur
        while player_hand.value < 21:
            action = agent.q_learning_choose_action(state)

            if action == 'h':
                hit(deck, player_hand)
                reward = 0.5 if player_hand.value < 21 else 0
                reward = -1 if player_hand.value > 21 else 0  # Perte si le joueur "bust"
            else:
                reward = 1
                break

            # Obtenir le nouvel état
            next_state = agent.get_state(player_hand.value, has_ace, dealer_card)

            # Mettre à jour la table Q
            agent.update_q_value(state, action, reward, next_state)

            state = next_state
            total_reward += reward

        # Jouer le tour du dealer si le joueur ne "bust" pas
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            # Déterminer le résultat
            # Récompenses Basiques
            if dealer_hand.value > 21 or player_hand.value > dealer_hand.value:
                reward = 1  # Victoire
            elif player_hand.value < dealer_hand.value:
                reward = -1  # Défaite
            else:
                reward = 0  # Égalité
                
            # Récompenses Optimisées 
            """if player_hand.value == 21:
                reward = 5  # Récompense élevée pour obtenir 21
            elif player_hand.value < 21:
                reward = 0.1 * player_hand.value / 21  # Récompense progressive
            elif player_hand.value < dealer_hand.value:
                reward = -1 # Défaite
            else:
                reward = 0.2 #Egaluté"""

            agent.update_q_value(state, action, reward, state)
            total_reward += reward

        # Réduire EPSILON pour favoriser l'exploitation
        EPSILON = max(QLearningBlackjackAgent.EPSILON * QLearningBlackjackAgent.EPSILON_DECAY, QLearningBlackjackAgent.EPSILON_MIN)
        # Enregistrer les statistiques
        scores.append(total_reward)
        final_hands.append(player_hand.value)

        # Afficher la progression
        print(f"Episode {episode + 1}/{episodes} completed. Récompense : {reward}")

    return agent, scores, final_hands
